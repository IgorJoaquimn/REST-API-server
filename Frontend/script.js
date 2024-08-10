document.addEventListener("DOMContentLoaded", function () {
  // Initial ID
  let currentId = 1;

  // Wait for the SVG to be loaded before executing
  const objectElement = document.querySelector("object");

  objectElement.addEventListener("load", function () {
    const svgDocument = objectElement.contentDocument; // Get the SVG document

    // Function to initialize all cannons as transparent
    function makeAllCannonsTransparent() {
      for (let row = 1; row <= 5; row++) {
        for (let column = 1; column <= 8; column++) {
          const id = `cannon ${row}_${column}`;
          const cannonElement = svgDocument.getElementById(id);
          if (cannonElement) {
            cannonElement.classList.add("transparent-group");
            cannonElement.classList.remove("show");
          }
        }
      }
    }

    // Initialize all cannons
    makeAllCannonsTransparent();

    // Function to update visibility based on the provided list
    function updateCannonVisibility(cannonList) {
      makeAllCannonsTransparent();
      // Remove transparency and add 'show' class to specified cannons
      cannonList.forEach(([row, column]) => {
        const id = `cannon ${column}_${row}`;
        const cannonElement = svgDocument.getElementById(id);
        if (cannonElement) {
          cannonElement.classList.add("show");
          cannonElement.classList.remove("transparent-group");
        }
      });
    }

    // Function to update the displayed game information
    function updateGameInfo(data) {
      document.getElementById('player-id').textContent = `Game id: ${data.game_id}`;
      document.getElementById('sunk-ships').textContent = `Sunk Ships: ${data.game_stats.sunk_ships}`;
      document.getElementById('escaped-ships').textContent = `Escaped Ships: ${data.game_stats.escaped_ships}`;
    }

    // Function to fetch and update cannons from backend
    function fetchCannons(id) {
      fetch(`http://127.0.0.1:5000/api/game/${id}`)
        .then(response => response.json())
        .then(data => {
          // Update the visibility and information based on the API response
          updateCannonVisibility(data.game_stats.cannons);
          updateGameInfo(data);
        })
        .catch(error => console.error('Error fetching data:', error));
    }

    // Initial fetch
    fetchCannons(currentId);

    // Add event listeners for buttons
    document.getElementById('prev-button').addEventListener('click', function () {
      if (currentId > 1) {
        currentId--;
        fetchCannons(currentId);
      }
    });

    document.getElementById('next-button').addEventListener('click', function () {
      currentId++;
      fetchCannons(currentId);
    });
  });
});
