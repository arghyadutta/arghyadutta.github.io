let searchIndex = [];

async function loadSearchIndex() {
    try {
        let response = await fetch("search-index.json");
        searchIndex = await response.json();
        console.log("Search index loaded!", searchIndex.length, "pages indexed.");
    } catch (error) {
        console.error("Failed to load search index:", error);
    }
}

function searchSite() {
    let query = document.getElementById("searchBox").value.trim().toLowerCase();
    let resultsContainer = document.getElementById("searchResults");
    resultsContainer.innerHTML = "";

    if (query.length < 2) return; // Ignore very short queries

    if (searchIndex.length === 0) {
        resultsContainer.innerHTML = "<li>Search index not loaded yet.</li>";
        return;
    }

    let results = searchIndex.filter(page =>
        page.title.toLowerCase().includes(query) ||
        page.content.toLowerCase().includes(query)
    );

    if (results.length === 0) {
        resultsContainer.innerHTML = "<li>No results found</li>";
    } else {
        results.forEach(page => {
            let listItem = document.createElement("li");
            listItem.innerHTML = `
                <a href="${page.url}">${highlightMatch(page.title, query)}</a> - 
                ${extractSnippets(page.content, query)}
            `;
            resultsContainer.appendChild(listItem);
        });
    }
}

function extractSnippets(text, query, snippetLength = 50) {
    if (!query) return text;

    // Escape the query to safely use it in a regex
    let escapedQuery = query.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&");
    let regex = new RegExp(escapedQuery, "gi");

    let matches = [...text.matchAll(regex)]; // Get all matches in the text
    let snippets = [];

    // Loop through all matches and extract the snippets
    matches.forEach(match => {
        // Get snippet from text around the match
        let start = Math.max(0, match.index - snippetLength);
        let end = Math.min(text.length, match.index + match[0].length + snippetLength);
        let snippet = text.substring(start, end);

        // Highlight the matched term within the snippet
        snippet = snippet.replace(regex, `<mark>$&</mark>`);

        // Convert line breaks to <br> tags
        // snippet = snippet.replace(/\n/g, "<br>");

        snippets.push(snippet); // Add the snippet to the list
    });

    // Return all snippets or a default message
    return snippets.length > 0 ? snippets.join("<br><br>") : "No matches found.";
}


function highlightMatch(text, query) {
    if (!query) return text; // Avoid modifying if no query

    // Replace line breaks with <br> to maintain formatting
    text = text.replace(/\n\n/g, "<br><br>").replace(/\n/g, "<br>");

    // Escape special characters in query for regex
    let escapedQuery = query.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&");

    // Create a regex that ensures **all** matches are found (global and case-insensitive)
    let regex = new RegExp(`(${escapedQuery})`, "gi");

    // Replace all matches with highlighted text
    return text.replace(regex, `<mark>$1</mark>`);
}


// Load search index when the page loads
document.addEventListener("DOMContentLoaded", loadSearchIndex);
