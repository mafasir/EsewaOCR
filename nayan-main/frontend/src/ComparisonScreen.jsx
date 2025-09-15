import React from 'react';

export function ComparisonScreen({ result, onBack, translations, language }) {
  const langContent = translations[language];

  const incorrectTextContent = Object.entries(result.original_data)
    .map(([key, value]) => `${key.replace(/_/g, ' ')}: ${value}`)
    .join('\n');

  return (
    <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-4xl border-2 border-green-200">
      <h2 className="text-3xl font-bold text-center mb-8 text-gray-800">{langContent.comparisonTitle}</h2>
      <div className="grid grid-cols-1 gap-y-5">
        <div>
          <label className="block text-gray-700 text-sm font-medium mb-2">{langContent.labels.incorrectTextLabel}</label>
          <textarea rows="10" className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50" value={incorrectTextContent} readOnly></textarea>
        </div>
        <div>
          <label className="block text-gray-700 text-sm font-medium mb-2">{langContent.labels.correctTextLabel}</label>
          <textarea rows="10" className="w-full px-4 py-3 border border-green-300 rounded-lg bg-green-50" defaultValue={result.corrected_text}></textarea>
        </div>
      </div>
      <div className="flex justify-end mt-8">
        <button type="button" onClick={onBack} className="px-8 py-3 rounded-full border-2 border-gray-400 text-gray-700 font-semibold text-lg shadow-md hover:bg-gray-100 transition-colors focus-ring-green">
          {langContent.buttons.backToFormBtn}
        </button>
      </div>
    </div>
  );
}