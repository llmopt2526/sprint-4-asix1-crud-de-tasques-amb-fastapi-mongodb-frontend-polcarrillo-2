const API_URL = "http://localhost:8000/llibres/";

document.addEventListener("DOMContentLoaded", () => {
    fetchBooks();
    document.getElementById("book-form").addEventListener("submit", createBook);
});

// Llistar tots els elements (R) [cite: 190]
async function fetchBooks() {
    const response = await fetch(API_URL);
    const books = await response.json();
    const list = document.getElementById("books-list");
    list.innerHTML = "";

    books.forEach(book => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${book.titol}</td>
            <td>${book.autor}</td>
            <td><span class="status-badge ${book.estat}">${book.estat}</span></td>
            <td>${book.valoracio}/10</td>
            <td>${book.persona}</td>
            <td>
                <button onclick="toggleStatus('${book._id}', '${book.estat}')">Canviar Estat</button>
                <button class="delete-btn" onclick="deleteBook('${book._id}')">Eliminar</button>
            </td>
        `;
        list.appendChild(row);
    });
}

// Crear un nou element (C) [cite: 189]
async function createBook(e) {
    e.preventDefault();
    const newBook = {
        titol: document.getElementById("titol").value,
        autor: document.getElementById("autor").value,
        categoria: document.getElementById("categoria").value,
        persona: document.getElementById("persona").value,
        valoracio: parseInt(document.getElementById("valoracio").value),
        estat: document.getElementById("estat").value
    };

    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newBook)
    });

    if (response.ok) {
        document.getElementById("book-form").reset();
        fetchBooks();
    }
}

// Editar/Canviar l'estat (U) [cite: 191, 194]
async function toggleStatus(id, currentStatus) {
    const nextStatus = currentStatus === "pendent" ? "llegit" : "pendent";
    const response = await fetch(`${API_URL}${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ estat: nextStatus })
    });

    if (response.ok) fetchBooks();
}

// Eliminar un element (D) [cite: 192]
async function deleteBook(id) {
    if (confirm("Segur que vols eliminar aquest llibre?")) {
        const response = await fetch(`${API_URL}${id}`, { method: "DELETE" });
        if (response.ok) fetchBooks();
    }
}
