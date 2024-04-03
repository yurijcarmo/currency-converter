"use client"
import axios from "axios";
import React, { useEffect, useState } from "react";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import dotenv from 'dotenv';

dotenv.config();

const Home = () => {
  const [currencies, setCurrencies] = useState([]);
  const [fromCurrency, setFromCurrency] = useState('');
  const [toCurrency, setToCurrency] = useState('');
  const [amount, setAmount] = useState('');
  const [convertedResult, setConvertedResult] = useState<null | string>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get(`${process.env.NEXT_PUBLIC_CURRENCY_API_URL}`)
      .then((response) => {
        if (response && response.data) {
          setCurrencies(response.data);
        } else {
          throw new Error('Invalid response');
        }
      })
      .catch((error) => toast.error('Error fetching currencies: ' + error));
  }, []);

  const convertCurrency = () => {
    if (!fromCurrency || !toCurrency || !amount) {
      toast.error('Por favor, preencha todos os campos.');
      return;
    }

    if (fromCurrency === toCurrency) {
      toast.error('A moeda de origem e a moeda de destino não podem ser iguais.');
      return;
    }

    setLoading(true);

    axios.get(`${process.env.NEXT_PUBLIC_CONVERT_API_URL}/?from=${fromCurrency}&to=${toCurrency}&amount=${amount}`)
      .then((response) => {
        if (response && response.data && response.data.converted_amount) {
          setConvertedResult(response.data.converted_amount);
        } else {
          throw new Error('Invalid response');
        }
      })
      .catch((error) => toast.error('Error converting currency: ' + error))
      .finally(() => setLoading(false));
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white bg-opacity-50 p-10 rounded-lg shadow-lg">
        <h1 className="text-4xl mb-8 text-center">Conversor Monetário</h1>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <h3 className="mb-2">De</h3>
            <select className="w-full p-2 border rounded-lg" onChange={e => setFromCurrency(e.target.value)} data-testid="from_currency">
              <option value="">Selecione</option>
              {currencies.map((currency: { code: string }) => (
                <option key={currency.code} value={currency.code}>{currency.code}</option>
              ))}
            </select>
          </div>
          <div>
            <h3 className="mb-2">Para</h3>
            <select className="w-full p-2 border rounded-lg" onChange={e => setToCurrency(e.target.value)} data-testid="to_currency">
              <option value="">Selecione</option>
              {currencies.map((currency: { code: string }) => (
                <option key={currency.code} value={currency.code}>{currency.code}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="flex items-center mb-4">
          <h3 className="mr-4">Valor</h3>
          <input type="number" className="w-full p-2 border rounded-lg" onChange={e => setAmount(e.target.value)} data-testid="amount" style={{ backgroundColor: 'rgba(255, 255, 255, 0.5)' }} />
        </div>
        <button className="bg-green-500 text-white py-2 px-4 rounded-lg w-full" onClick={convertCurrency} disabled={loading} data-testid="converter">Converter</button>
        {loading && <p className="mt-4 text-center">Atualizando tabela de cotações, pode demorar alguns minutos...</p>}
        {convertedResult !== null && <p className="fs-3 mt-4" >O valor convertido é aproximadamente ==&gt; {convertedResult}</p>}
        <ToastContainer />
      </div>
    </div>
  );
}

export default Home;
