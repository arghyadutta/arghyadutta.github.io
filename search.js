let searchIndex = [];

async function loadSearchIndex() {
    try {
        let response = await fetch("search-index.json");
        searchIndex = await response.json();
        console.log("Search index loaded!");
    } catch (error) {
        console.error("Failed to load search index:", error);
    }
}

function searchSite() {
    let query = document.getElementById("searchBox").value.trim().toLowerCase();
    let resultsContainer = document.getElementById("searchResults");
    resultsContainer.innerHTML = "";

    if (query.length < 2) return; // Ignore short queries

    let results = searchIndex.filter(page => 
        page.title.toLowerCase().includes(query) || 
        page.content.toLowerCase().includes(query)
    );

    if (results.length === 0) {
        resultsContainer.innerHTML = "<li>No results found</li>";
    } else {
        results.forEach(page => {
            let listItem = document.createElement("li");
            listItem.innerHTML = `<a href="${page.url}">${highlightMatch(page.title, query)}</a> - ${highlightMatch(page.content.substring(0, 500), query)}...`;
            resultsContainer.appendChild(listItem);
        });
    }
}

// Highlight function to show matches
function highlightMatch(text, query) {
    let regex = new RegExp(`(${query})`, "gi");
    return text.replace(regex, `<mark>$1</mark>`);
}

// Load search index when the page loads
document.addEventListener("DOMContentLoaded", loadSearchIndex);
