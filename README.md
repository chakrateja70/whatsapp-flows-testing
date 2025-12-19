# WhatsApp Flows FastAPI Server

A production-ready FastAPI server for WhatsApp Flows integration with encryption/decryption support.

## Features

- ✅ FastAPI async server
- ✅ Request signature validation (HMAC SHA256)
- ✅ RSA + AES-GCM encryption/decryption
- ✅ Flow state management
- ✅ Health check endpoint
- ✅ Environment variable configuration
- ✅ Type hints and documentation

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate RSA Keys

```bash
python key_generator.py YourSecurePassphrase
```

Copy the output to your `.env` file.

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
- `APP_SECRET` - From WhatsApp App Dashboard
- `PRIVATE_KEY` - Generated from step 2
- `PASSPHRASE` - Used in step 2
- `PORT` - Server port (default: 3000)

### 4. Upload Public Key

Upload the public key (generated in step 2) to WhatsApp:
- Go to WhatsApp Manager
- Navigate to your Flow
- Upload the public key in Settings

### 5. Run Server

```bash
# Development
python server.py

# Production (with auto-reload)
uvicorn server:app --host 0.0.0.0 --port 3000 --reload

# Production (multiple workers)
uvicorn server:app --host 0.0.0.0 --port 3000 --workers 4
```

## Project Structure

```
.
├── server.py           # FastAPI server and endpoints
├── encryption.py       # Encryption/decryption logic
├── flow.py            # Flow business logic
├── key_generator.py   # RSA key pair generator
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (create from .env.example)
└── README.md         # This file
```

## API Endpoints

### `POST /`
Main endpoint for WhatsApp Flows webhook.

**Headers:**
- `x-hub-signature-256`: HMAC SHA256 signature

**Request Body:**
```json
{
  "encrypted_aes_key": "base64_encoded_key",
  "encrypted_flow_data": "base64_encoded_data",
  "initial_vector": "base64_encoded_iv"
}
```

### `GET /`
Returns simple HTML message.

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "whatsapp-flows-endpoint"
}
```

## Flow Screens

The example flow includes these screens:
1. **APPOINTMENT** - Select department, location, date, time
2. **DETAILS** - Enter name, email, phone, additional details
3. **SUMMARY** - Review appointment details
4. **SUCCESS** - Confirmation

Modify `flow.py` to customize your flow logic.

## Security

- ✅ Request signature validation with HMAC SHA256
- ✅ RSA-2048 key pair for AES key exchange
- ✅ AES-128-GCM for data encryption
- ✅ Passphrase-protected private key
- ✅ Environment variable for secrets

## Development

### Run with auto-reload
```bash
uvicorn server:app --reload
```

### Run tests
```bash
pytest
```

### Format code
```bash
black .
```

## Deployment

### Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "3000"]
```

Build and run:
```bash
docker build -t whatsapp-flows .
docker run -p 3000:3000 --env-file .env whatsapp-flows
```

### Cloud Platforms

- **AWS**: Deploy to Elastic Beanstalk, ECS, or Lambda
- **Azure**: Deploy to App Service or Container Instances
- **GCP**: Deploy to Cloud Run or App Engine
- **Railway/Render**: Direct deployment from Git

## Troubleshooting

### Signature validation fails
- Verify `APP_SECRET` matches WhatsApp App Dashboard
- Check request is being sent from WhatsApp
- Ensure raw body is used for signature calculation

### Decryption fails (421 error)
- Verify `PRIVATE_KEY` and `PASSPHRASE` are correct
- Ensure public key uploaded to WhatsApp matches private key
- Check key format (PEM with proper headers)

### Flow not responding
- Check server logs for errors
- Verify endpoint URL is publicly accessible
- Test health check endpoint
- Review flow.py logic for unhandled cases

## License

MIT License - Copyright (c) Meta Platforms, Inc. and affiliates.

## Resources

- [WhatsApp Flows Documentation](https://developers.facebook.com/docs/whatsapp/flows)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WhatsApp Business Platform](https://business.whatsapp.com/)
