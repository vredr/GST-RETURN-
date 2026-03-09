# TaxNow - GST Compliance SaaS Platform

AI-powered GST automation platform that converts raw marketplace sales data into GST-compliant returns for Indian businesses.

## Features

- **11 Marketplaces Supported**: Amazon, Flipkart, Meesho, Shopify, WooCommerce, Snapdeal, IndiaMART, AJIO, Myntra, JioMart, Generic Excel
- **13 GST Returns**: GSTR-1, GSTR-3B, GSTR-2A, GSTR-2B, GSTR-4, GSTR-5, GSTR-6, GSTR-7, GSTR-8, GSTR-9, GSTR-9C, GSTR-10, GSTR-11
- **Auto Column Detection**: Smart mapping of marketplace columns to GST schema
- **GST Classification**: Automatic B2B, B2CL, B2CS classification
- **Tax Calculation**: Accurate CGST, SGST, IGST computation
- **Excel Export**: Download GST-ready Excel files

## Tech Stack

### Backend
- Python 3.11 + FastAPI
- MongoDB Atlas (async with Motor)
- Pandas for data processing
- OpenPyXL for Excel generation

### Frontend
- React 18 + TypeScript + Vite
- Tailwind CSS
- shadcn/ui components

## Deployment

### Backend (Railway)
1. Connect Railway to GitHub repo
2. Set environment variables:
   ```
   MONGODB_URI=your_mongodb_uri
   SECRET_KEY=your_secret_key
   ```
3. Deploy

### Frontend (Vercel)
1. Import project from GitHub
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Set environment variable:
   ```
   VITE_API_URL=https://your-railway-app.up.railway.app
   ```
5. Deploy

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload marketplace Excel |
| POST | `/process` | Process and normalize data |
| GET | `/generate-return` | Generate any GST return |
| GET | `/marketplaces` | List supported marketplaces |
| GET | `/return-types` | List GST return types |
| GET | `/health` | Health check |

## GST Logic

### Classification Rules
- **B2B**: Customer has GSTIN
- **B2CL**: No GSTIN + Interstate + Value > ₹2.5L
- **B2CS**: Everything else

### Tax Calculation
```
Intrastate: CGST = Taxable × Rate/2, SGST = Taxable × Rate/2
Interstate:  IGST = Taxable × Rate
```

## License

MIT License
