"use client";

import React, { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface NseData {
  spot: number;
  ce_oi: number;
  pe_oi: number;
  pcr: number;
  timestamp: string;
}

export default function Home() {
  const [symbol, setSymbol] = useState("NIFTY");
  const [data, setData] = useState<NseData | null>(null);
  const [loading, setLoading] = useState(false);

  async function fetchData() {
    try {
      setLoading(true);
      const res = await fetch(`/api/nse?symbol=${symbol}`);
      if (!res.ok) throw new Error("API error");
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
    const id = setInterval(fetchData, 20000); // <-- 20 seconds refresh
    return () => clearInterval(id);
  }, [symbol]);

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center gap-4">
        <select
          className="border p-2 rounded"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
        >
          <option value="NIFTY">NIFTY</option>
          <option value="BANKNIFTY">BANKNIFTY</option>
        </select>
        <Badge>Spot: {data?.spot ?? "--"}</Badge>
        <Badge>CE OI: {data?.ce_oi ?? "--"}</Badge>
        <Badge>PE OI: {data?.pe_oi ?? "--"}</Badge>
        <Badge>PCR: {data?.pcr ?? "--"}</Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Live from NSE (refreshes every 20s)</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Timestamp: {data?.timestamp ?? "--"}</p>
        </CardContent>
      </Card>
    </div>
  );
}
