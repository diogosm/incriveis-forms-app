async function populateTable() {
  try {
    const response = await fetch('http://localhost:5000/pacientesData'); // Replace with your actual API endpoint
    console.log(response)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const authorsData = await response.json();

    const authorsTableBody = document.getElementById('authors-table-body');

    authorsData.forEach(authorData => {
      const row = document.createElement('tr');

      // Create table cells based on author data
      const authorCell = createAuthorCell(authorData);
      const functionCell = createFunctionCell(authorData);
      const statusCell = createStatusCell(authorData);
      const createdDateCell = createCreatedDateCell(authorData.date_created);
      const updatedDateCell = createUpdatedDateCell(authorData.date_updated);

      row.appendChild(authorCell);
      row.appendChild(functionCell);
      row.appendChild(statusCell);
      row.appendChild(createdDateCell);
      row.appendChild(updatedDateCell);

      authorsTableBody.appendChild(row);
    });
  } catch (error) {
    console.error('Error fetching data:', error);
    // Handle errors gracefully, e.g., display an error message to the user
  }
}

function createAuthorCell(authorData) {
  const cell = document.createElement('td');

  // Assuming 'nome' is the author name in your data structure
  const authorName = authorData.nome || 'N/A'; // Handle missing data gracefully

  const authorContent = document.createElement('div');
  authorContent.classList.add('d-flex', 'px-2');

  const authorImage = document.createElement('img');
  authorImage.classList.add('avatar', 'avatar-sm', 'rounded-circle', 'me-2');
  authorImage.src = '../assets/img/small-logos/default-avatar.svg'; // Replace with default avatar path or logic to use specific image based on data

  const authorDetails = document.createElement('div');
  authorDetails.classList.add('my-auto');

  const authorNameElement = document.createElement('h6');
  authorNameElement.classList.add('mb-0', 'text-sm');
  authorNameElement.textContent = authorName;

  authorDetails.appendChild(authorNameElement);
  authorContent.appendChild(authorImage);
  authorContent.appendChild(authorDetails);

  cell.appendChild(authorContent);

  return cell;
}

function createFunctionCell(authorData) {
  const cell = document.createElement('td');
  const functionText = document.createElement('p');
  functionText.classList.add('text-sm', 'font-weight-bold', 'mb-0');

  // Assuming 'funcao' (Portuguese for "function") is the field for function data
  const functionValue = authorData.funcao || 'N/A'; // Handle missing data gracefully
  functionText.textContent = `$${functionValue}`; // Assuming function value is a number

  cell.appendChild(functionText);

  return cell;
}

function createStatusCell(authorData) {
  const cell = document.createElement('td');
  const cellText = document.createElement('span');
  cellText.classList.add('text-xs', 'font-weight-bold', 'mb-0');

  // Assuming 'status' is the field for status data
  const statusValue = authorData.status || 'N/A'; // Handle missing data gracefully
  cellText.textContent = statusValue;

  cell.classList.add('align-middle', 'text-center');
  cell.appendChild(cellText);

  return cell;
}

function createCreatedDateCell(createdDate) {
  const cell = document.createElement('td');
  const cellText = document.createElement('span');
  cellText.classList.add('text-xs', 'font-weight-bold', 'mb-0');

  // You can format the date here using libraries like moment.js or Date.prototype.toLocaleDateString()
  cellText.textContent = createdDate;

  cell.classList.add('align-middle', 'text-center');
  cell.appendChild(cellText);

  return cell;
}

function createUpdatedDateCell(updatedDate) {
  const cell = document.createElement('td');
  const cellText = document.createElement('span');
  cellText.classList.add('text-xs', 'font-weight-bold', 'mb-0');

  // You can format the date here using libraries like moment.js or Date.prototype.toLocaleDateString()
  cellText.textContent = updatedDate;

  cell.classList.add('align-middle', 'text-center');
  cell.appendChild(cellText);

  return cell;
}

// Call the function to populate the table
populateTable();