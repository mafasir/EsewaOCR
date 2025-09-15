import React from 'react';

export function WelcomeScreen({ onStart }) {
  return (
    <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-2xl text-center border-2 border-green-200">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">Welcome to Nayan</h1>
      <p className="text-gray-600 mb-8 leading-relaxed">
        Nayan is a Post-OCR correction tool using Transformers to fix errors in text extracted by OCR systems. It treats correction as a sequence-to-sequence task, converting noisy OCR output into clean, accurate text.
      </p>
      <button
        onClick={onStart}
        className="px-8 py-4 rounded-full parrot-green text-white font-semibold text-xl shadow-md hover:opacity-90 transition-opacity focus-ring-green"
      >
        Start
      </button>
    </div>
  );
}