import React, { useState } from 'react';
import axios from 'axios';
import { WelcomeScreen } from './WelcomeScreen';
import { KycForm } from './KycForm';
import { ComparisonScreen } from './ComparisonScreen';
import { translations } from './translation'; 

const FASTAPI_ENDPOINT_ENGLISH = "http://127.0.0.1:8000/kyc/english/";
const FASTAPI_ENDPOINT_NEPALI = "http://127.0.0.1:8000/kyc/nepali/";

function App() {
  const [view, setView] = useState('welcome');
  const [apiResult, setApiResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [language, setLanguage] = useState('en');

  const handleApiSubmit = async (formData, lang) => {
    setIsLoading(true);
    setError('');
    setApiResult(null);

    const isNepali = lang === 'np';
    const endpoint = isNepali ? FASTAPI_ENDPOINT_NEPALI : FASTAPI_ENDPOINT_ENGLISH;

    console.log(`Submitting to ${endpoint} for language: ${lang}`);

    try {
      const response = await axios.post(endpoint, formData);
      setApiResult(response.data);
      setView('comparison');
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || "An unknown error occurred.";
      setError(`API Error: ${errorMsg}`);
    } finally {
      setIsLoading(false);
    }
  };

  const renderCurrentView = () => {
    switch (view) {
      case 'form':
        return (
          <KycForm
            onCorrect={handleApiSubmit}
            onBack={() => setView('welcome')}
            isLoading={isLoading}
            translations={translations}
            language={language}
            setLanguage={setLanguage}
          />
        );
      case 'comparison':
        return (
          <ComparisonScreen
            result={apiResult}
            onBack={() => setView('form')}
            translations={translations}
            language={language}
          />
        );
      default:
        return (
          <WelcomeScreen
            onStart={() => setView('form')}
            language={language}
            setLanguage={setLanguage}
            translations={translations}
          />
        );
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen p-4 bg-gray-100">
      {error && <div className="absolute top-10 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded" role="alert">{error}</div>}
      {renderCurrentView()}
    </div>
  );
}

export default App;