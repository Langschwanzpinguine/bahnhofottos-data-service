# Bahnhofottos Data Service API

This API provides endpoints for managing and updating data related to countries and global data. It allows you to refresh data, add countries of interest, delete countries from the list, and more.


### Endpoints
#### Refresh All Data

- Route: `POST /refresh/all`
- Description: Refreshes all data, including global data and countries of interest.
- Usage: Use this endpoint to update all data.
- Example Request:


```sh
curl -X POST http://localhost:8080/refresh/all
```

- Response: No content (HTTP status code 204).

#### Refresh Countries

- Route: `POST /refresh/countries`
- Description: Refreshes data for specific countries.
- Usage: rovide a JSON body with a list of ISO 3166-1 country codes to refresh.
- Example Request:

```sh
curl -X POST -H "Content-Type: application/json" -d '{"countries":["CH", "DE"]}' http://localhost:8080/refresh/countries
```

- Response: No content (HTTP status code 204).

#### Refresh All Countries

- Route: `POST /refresh/all_countries`
- Description: Refreshes data for all countries of interest.
- Usage: Use this endpoint to update data for all countries.
- Example Request:

```sh
curl -X POST http://localhost:8080/refresh/all_countries
```

- Response: No content (HTTP status code 204).

#### Add Countries

- Route: `POST /add_countries`
- Description: Adds new countries to the list of countries of interest.
- Usage: Provide a JSON body with a list of ISO 3166-1 country codes to add. Optionally, you can set `refresh_now` to `true` to immediately refresh data for the added countries.
- Example Request:

```sh
curl -X POST -H "Content-Type: application/json" -d '{"countries": ["AT"], "refresh_now": true}' http://localhost:8080/add_countries
```

- Response: No content (HTTP status code 204).

#### Delete Countries

- Route: `POST /delete_countries`
- Description: Deletes countries from the list of countries of interest.
- Usage: Provide a JSON body with a list of ISO 3166-1 country codes to delete.
- Example Request:

```sh
curl -X POST -H "Content-Type: application/json" -d '{"countries": ["DE"]}' http://localhost:8080/delete_countries
```
- Response: No content (HTTP status code 204).

#### Notes
Dont refresh the data at high frequencies
