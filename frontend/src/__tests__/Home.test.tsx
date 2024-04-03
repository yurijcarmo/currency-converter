import React from 'react';
import { render, waitFor, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom'
import axios from 'axios';
import Home from '../app/page';

jest.mock('axios');

describe('Page component', () => {
  beforeEach(() => {
    (axios.get as jest.Mock).mockResolvedValueOnce(
      { data: [{ code: 'USD' }, { code: 'EUR' }] }
    );
  });

  test('renders the component with initial state', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/Conversor Monetário/i)).toBeInTheDocument();
      expect(screen.getByText('De')).toBeInTheDocument();
      expect(screen.getByText('Para')).toBeInTheDocument();
      expect(screen.getByText('Valor')).toBeInTheDocument();
      expect(screen.getByText('Converter')).toBeInTheDocument();
    });
  });

  test('fetches currencies on component mount', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledTimes(2);
      expect(axios.get).toHaveBeenCalledWith(process.env.NEXT_PUBLIC_CURRENCY_API_URL);
    });
  });

  test('converts currency when button is clicked', async () => {
    render(<Home />);

    await waitFor(async () => {
      const selectFromCurrency = screen.getByTestId('from_currency');
      const selectToCurrency = screen.getByTestId('to_currency');
      const inputAmount = screen.getByTestId('amount');

      fireEvent.change(selectFromCurrency, { target: { value: 'USD' } });
      fireEvent.change(selectToCurrency, { target: { value: 'EUR' } });
      fireEvent.change(inputAmount, { target: { value: '100' } });

      fireEvent.click(screen.getByTestId('converter'));

      (axios.get as jest.Mock).mockResolvedValueOnce({ data: { converted_amount: 123.45 } });

      expect(axios.get).toHaveBeenCalledWith(`${process.env.NEXT_PUBLIC_CONVERT_API_URL}/?from=USD&to=EUR&amount=100`);
    });
  });
});