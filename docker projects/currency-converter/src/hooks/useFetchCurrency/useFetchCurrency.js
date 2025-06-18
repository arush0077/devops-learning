import { useState, useEffect, useRef, useCallback } from 'react';
import { buildApiUrl } from '@/lib/buildApiUrl';
import { mapCurrencyData } from '@/lib/mappers';

const useFetchCurrency = (baseCurrency, targetCurrency) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const cache = useRef({});

  const fetchCurrencyData = useCallback(async () => {
    setLoading(true);
    setError(null);
    const url = buildApiUrl(baseCurrency, targetCurrency, 30);
    if (cache.current[url]) {
      setData(cache.current[url]);
      setLoading(false);
      return;
    }
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Erro ao buscar os dados');
      }
      const result = await response.json();
      const mappedData = mapCurrencyData(result);
      cache.current[url] = mappedData;
      setData(mappedData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [baseCurrency, targetCurrency]);
  useEffect(() => {
    fetchCurrencyData();
  }, [fetchCurrencyData]);

  return { data, loading, error };
};

export default useFetchCurrency;
