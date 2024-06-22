package main

import (
	"fmt"
	"net/http"
	"path/filepath"
)

func main() {
    http.Handle("/", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if r.URL.Path != "/" {
            http.NotFound(w, r)
            panic("404 Not Found")
        }
        indexPath := filepath.Join("..", "index.html")
        http.ServeFile(w, r, indexPath)
    }))

    fmt.Println("Starting server on :8080")

    err := http.ListenAndServe(":8080", nil)
    if err != nil {
        panic("Error starting server: " + err.Error())
    }
}
