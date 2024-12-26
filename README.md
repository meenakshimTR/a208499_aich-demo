## ASP support Python Fast API.

## Prerequisites

* Git
* Python 3.7
* Docker
* Postman

## Getting Started

- Clone the repository.
    ```shell
    git clone https://github.com/tr/ASP_CLI.git
    ```

# Docker image.

- App location

````
  src/programs/python-app
````

- Build the image.
  ```shell
  docker build -t tr/asp-python-app .
  ```
- Run the image.
  ```shell
  docker run -it -p 8080:8080 tr/asp-python-app
  ```

## Endpoints

- CURL POST endpoint for concept

````
curl --location --request POST 'localhost:8080/concepts/v1/slug' \
   --header 'Authorization: Bearer '
````

- CURL POST endpoint for agents

````
curl --location --request POST 'localhost:8080/agents/v1/slug' \
   --header 'Authorization: Bearer '
````
