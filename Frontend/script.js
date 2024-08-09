document.addEventListener("DOMContentLoaded", function() {
    // Initial ID
    let currentId = 1;
  
    // Wait for the SVG to be loaded before executing
    const objectElement = document.querySelector("object");
    
    objectElement.addEventListener("load", function() {
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
        // Remove transparency and add 'show' class to specified cannons
        cannonList.forEach(([row, column]) => {
          const id = `cannon ${row}_${column}`;
          const cannonElement = svgDocument.getElementById(id);
          if (cannonElement) {
            cannonElement.classList.add("show");
            cannonElement.classList.remove("transparent-group");
          }
        });
      }
  
      // Function to fetch and update cannons from backend
      function fetchCannons(id) {
        fetch(`/api/game/${id}`)
          .then(response => response.json())
          .then(data => {
            // Assume `data` is the list of cannons to show
            updateCannonVisibility(data.cannons); // Update the visibility
          })
          .catch(error => console.error('Error fetching data:', error));
      }
  
      // Initial fetch
      fetchCannons(currentId);
  
      // Function to handle scroll events
      function handleScroll() {
        if (window.scrollY > lastScrollTop) {
          // Scrolling down
          currentId++;
        } else {
          // Scrolling up
          currentId = Math.max(1, currentId - 1); // Prevent going below ID 1
        }
        lastScrollTop = window.scrollY <= 0 ? 0 : window.scrollY;
  
        // Fetch and update cannons based on new ID
        fetchCannons(currentId);
      }
  
      let lastScrollTop = 0;
      window.addEventListener("scroll", handleScroll);
    });
  });
  