import { API_URL } from '../../constants';

export const buildApiUrl = (baseCurrency, targetCurrency, period) => {
  const endDate = new Date().toISOString().split('T')[0];
  const startDate = new Date(new Date().setDate(new Date().getDate() - period))
    .toISOString()
    .split('T')[0];

  return `${API_URL}&base=${baseCurrency}&start_date=${startDate}&end_date=${endDate}&symbols=${targetCurrency}`;
};
