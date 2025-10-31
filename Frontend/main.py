#!/usr/bin/env python3
from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource
from flask_cors import CORS

import os
import sys

import signal
import psutil

import subprocess as sp

import argparse

import re
import json

from tqdm import tqdm

import devtrans as dt



def my_sandhi_split(word: str):
    sentence_modes = {
        "sent" : "t",
        "word" : "f"
    }

    segmentation_modes = {
        "first" : "s",
        "best" : "l"
    }

    cgi_file = "./interface2"
        

    def get_user_input():
        print("=== Sanskrit Heritage Segmenter ===\n")

        input_enc = "RN"

        output_enc = "deva"

        sent_mode = "sent"

        seg_mode = "best"

        input_type = "text"

        
        input_text = word
        

        return input_enc, output_enc, sent_mode, seg_mode, input_type, input_text 

    def handle_input(input_text, input_encoding):
        """ Modifies input based on the requirement of the Heritage Engine
        """
        
        # Replace special characters with "." since Heritage Segmenter
        # does not accept special characters except "|", "!", "."
        modified_input = re.sub(r'[$@#%&*()\[\]=+:;"}{?/,\\]', ' ', input_text)
        if not (input_encoding == "RN"):
            modified_input = modified_input.replace("'", " ")
        
        normalized_input = re.sub(r'M$', 'm', modified_input)
        normalized_input = re.sub(r'\.m$', '.m', normalized_input)
        
        return normalized_input


    def input_transliteration(input_text, input_enc):
        """ Converts input in any given notation to WX  
        """
        
        trans_input = ""
        trans_enc = ""
        
        if input_enc == "DN":
            trans_input = dt.dev2wx(input_text)
            trans_input = trans_input.replace("ळ", "d")
            trans_enc = "WX"
        elif input_enc == "RN":
            trans_input = dt.iast2wx(input_text)
            trans_enc = "WX"
        else:
            trans_input = input_text
            trans_enc = input_enc
            
        # The following condition makes sure that the other chandrabindu
        # which comes on top of other characters is replaced with m
        if "z" in trans_input:
            if trans_input[-1] == "z":
                trans_input = trans_input.replace("z", "m")
            else:
                trans_input = trans_input.replace("z", "M")
        
        return (trans_input, trans_enc)


    def output_transliteration(output_text, output_enc):
        """ Converts the output which is always in WX to 
            deva or roma
        """
        
        trans_output = ""
        trans_enc = ""
        
        if output_enc == "deva":
            trans_output = dt.wx2dev(output_text)
            trans_enc = "deva"
        elif output_enc == "roma":
            trans_output = dt.wx2iast(output_text)
            trans_enc = "roma"
        else:
            trans_output = output_text
            trans_enc = output_enc
        
        return (trans_output, trans_enc)


    def run_sh(cgi_file, input_text, input_encoding, lex="MW", sentence_mode="t",
                us="f", output_encoding="roma", segmentation_mode="l",
                pipeline="t"):
        """ Runs the cgi file with a given word/sentence.  
            
            Returns a JSON
        """
        
        time_out = 30
        
        out_enc = output_encoding if output_encoding in ["roma", "deva"] else "roma"
        
        env_vars = [
            "lex=" + lex,
            "st=" + sentence_mode,
            "us=" + us,
            "font=" + out_enc,
            "t=" + input_encoding,
            "text=" + input_text,#.replace(" ", "+"),
            "mode=" + segmentation_mode,
            "pipeline=" + pipeline
        ]
        
        query_string = "QUERY_STRING=\"" + "&".join(env_vars) + "\""
        command = query_string + " " + cgi_file
        
        try:
            p = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            outs, errs = p.communicate(timeout=time_out)
        except sp.TimeoutExpired:
            parent = psutil.Process(p.pid)
            for child in parent.children(recursive=True):
                child.terminate()
                parent.terminate()
            result = ""
            status = "Timeout"
        except Exception as e:
            result = ""
            status = "Failure"
        else:
            result = outs.decode('utf-8')
            status = "Success"
        
        return result, status
        

    def handle_result(input_sent, result, status, output_encoding):
        """ Returns the results from the JSON
        """
        
        result_json = {}
        
        trans_input = output_transliteration(input_sent, output_encoding)[0]
        
        if status == "Success":
            try:
                result_str = result.split("\n")[-1]
                result_json = json.loads(result_str)
            except Exception as e:
                result_json = {}
        
            segs = result_json.get("segmentation", [ input_sent ])
            
            if "error" in segs[0]:
                trans_segs = [ "Error: " + trans_input ]
            else:
                trans_segs = [ output_transliteration(seg, output_encoding)[0] for seg in segs ]
        elif status == "Timeout":
            trans_segs = [ ("Timeout: " + trans_input) ]
        elif status == "Failure":
            trans_segs = [ ("Failure: " + trans_input) ]
        else:
            trans_segs = [ ("Unknown: " + trans_input) ]
        
        return trans_segs
        

    def run_sh_text(cgi_file, input_sent, input_encoding, lex="MW",
                    sentence_mode="t", us="f", output_encoding="roma",
                    segmentation_mode="l", pipeline="t"):
        """ Handles segmentation for the given input sentence
        """
        
        # SH does not accept special characters in the input sequence.  
        # And it results errors if such characters are found.  
        # Uncomment the following to segment the sentence by ignoring  
        # the special characters.  Currently, the following is commented
        # and the same input is returned as the output.
        
        input_sent = handle_input(input_sent.strip(), input_encoding)
        
        trans_input, trans_enc = input_transliteration(input_sent, input_encoding)
        
        result, status = run_sh(
            cgi_file, trans_input, trans_enc, lex, sentence_mode, us,
            output_encoding, segmentation_mode, pipeline
        )
        
        segmentation = handle_result(input_sent, result, status, output_encoding)
        print(segmentation)
        return segmentation


    def main():
        input_enc, output_enc, sent_mode, seg_mode, input_type, input_text = get_user_input()

        sent_mode_code = sentence_modes.get(sent_mode, "t")
        seg_mode_code = segmentation_modes.get(seg_mode, "s")
        
        return run_sh_text(
            cgi_file, input_text, input_enc, lex="MW",
            sentence_mode=sent_mode_code, us="f", output_encoding=output_enc,
            segmentation_mode=seg_mode_code, pipeline="t"
        )
        

    
    return main()

my_sandhi_split("sa guruḥ lateva gacchati")