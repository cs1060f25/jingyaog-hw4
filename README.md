# County Health Rankings API

A serverless API for querying county health rankings data by ZIP code and health measure.

## API Endpoint

**URL:** `https://jingyaog-hw4.vercel.app/api/county_data`
**Method:** POST
**Content-Type:** `application/json`

## Request Format

```json
{
  "zip": "02138",
  "measure_name": "Unemployment"
}
```

### Required Parameters

- `zip` (string): 5-digit ZIP code
- `measure_name` (string): Must be one of:
  - "Violent crime rate"
  - "Unemployment"
  - "Children in poverty"
  - "Diabetic screening"
  - "Mammography screening"
  - "Preventable hospital stays"
  - "Uninsured"
  - "Sexually transmitted infections"
  - "Physical inactivity"
  - "Adult obesity"
  - "Premature Death"
  - "Daily fine particulate matter"

### Easter Egg

Include `"coffee": "teapot"` in the request to receive an HTTP 418 response.

## Response Format

Returns county health rankings data in JSON format matching the original database schema.

## Error Codes

- **400**: Missing or invalid parameters
- **404**: No data found or invalid endpoint
- **418**: Coffee teapot easter egg
- **500**: Internal server error

## Example Usage

```bash
curl -X POST https://jingyaog-hw4.vercel.app/api/county_data \
  -H "Content-Type: application/json" \
  -d '{"zip": "02138", "measure_name": "Unemployment"}'
```

## Deployment

Deployed on Vercel as serverless functions. The API automatically connects to the SQLite database and performs JOIN queries between ZIP code and county health rankings tables.