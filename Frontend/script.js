// Example API fetch (replace URL with your API)
fetch('http://127.0.0.1:9000/sanskrit_parser/v1/tags/पुष्पं')
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById('data-container');

    data.forEach(item => {
      // Create a div for each item
      const div = document.createElement('div');
      div.classList.add('data-item');
      div.textContent = item.name; // main text shown

      // Create tooltip div
      const tooltip = document.createElement('div');
      tooltip.classList.add('tooltip');
      tooltip.textContent = JSON.stringify(item, null, 2); // JSON data formatted

      // Append tooltip inside data-item div
      div.appendChild(tooltip);
      container.appendChild(div);
    });
  })
  .catch(error => console.error(error));
