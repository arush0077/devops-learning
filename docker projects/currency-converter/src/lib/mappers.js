export const mapCurrencyData = (apiResponse) => {
  const result = [];

  const data = apiResponse.response;

  for (const [date, valueObject] of Object.entries(data)) {
    const value = Object.values(valueObject)[0];
    result.push({
      date,
      value: parseFloat(value).toFixed(2),
    });
  }

  return result;
};
