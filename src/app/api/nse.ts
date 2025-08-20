import type { NextApiRequest, NextApiResponse } from "next";
import fetch from "node-fetch";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { symbol } = req.query;
  if (!symbol) return res.status(400).json({ error: "Missing symbol" });

  try {
    // NSE Option Chain API
    const url = `https://www.nseindia.com/api/option-chain-indices?symbol=${symbol}`;
    const response = await fetch(url, {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
      },
    });

    if (!response.ok) {
      return res.status(response.status).json({ error: "NSE API error" });
    }

    const json = await response.json();
    const records = json.records?.data || [];
    const underlyingValue = json.records?.underlyingValue || null;

    let ceOI = 0;
    let peOI = 0;
    records.forEach((item: any) => {
      if (item.CE) ceOI += item.CE.openInterest || 0;
      if (item.PE) peOI += item.PE.openInterest || 0;
    });

    const pcr = peOI && ceOI ? (peOI / ceOI).toFixed(2) : null;

    res.status(200).json({
      spot: underlyingValue,
      ce_oi: ceOI,
      pe_oi: peOI,
      pcr: pcr,
      timestamp: new Date().toLocaleTimeString(),
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
}
