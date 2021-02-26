1) Build container:
    ```
    docker build -t telephones:latest .
    ```

2) Copy test file or create new with the same name:
    ```
    cp test.csv sites.csv
    ```

3) Run container with file input:
    ```
    docker run --rm -v $(pwd)/sites.csv:/usr/src/telephones/sites.csv -t telephones:latest -f "sites.csv"
    ```
    or with a list of urls as command's arguments
    ```
    docker run --rm -t telephones:latest "https://masterdel.ru" "https://repetitors.info"
    ```
