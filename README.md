1) Build container:
    ```
    docker build -t telephones:latest .
    ```

2) Copy test file or create new with the same name:
    ```
    cp test.csv sites.csv
    ```

3) Run container:
    ```
    docker run -v $(pwd)/sites.csv:/usr/src/telephones/sites.csv -t telephones:latest -f "sites.csv"
    ```
