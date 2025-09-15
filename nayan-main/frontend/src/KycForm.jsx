import React, { useState } from "react";

export function KycForm({
  onCorrect,
  onBack,
  isLoading,
  translations,
  language,
  setLanguage,
}) {
  const [formData, setFormData] = useState({
    id_number: "",
    name: "",
    dob: "",
    gender: "Male",
    district: "",
    municipality: "",
    father_name: "",
    mother_name: "",
  });

  const langContent = translations[language];

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onCorrect(formData, language);
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-4xl border-2 border-green-200">
      <div className="flex justify-center mb-6 space-x-4">
        <button
          onClick={() => setLanguage("en")}
          className={`px-6 py-3 rounded-full font-semibold text-lg shadow-md transition-all focus-ring-green ${
            language === "en"
              ? "parrot-green text-white"
              : "border-2 border-parrot-green text-parrot-green-text hover:bg-green-50"
          }`}
        >
          English
        </button>
        <button
          onClick={() => setLanguage("np")}
          className={`px-6 py-3 rounded-full font-semibold text-lg shadow-md transition-all focus-ring-green ${
            language === "np"
              ? "parrot-green text-white"
              : "border-2 border-parrot-green text-parrot-green-text hover:bg-green-50"
          }`}
        >
          नेपाली
        </button>
      </div>

      <h2 className="text-3xl font-bold text-center mb-8 text-gray-800">
        {langContent.formTitle}
      </h2>

      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-5">
          {[
            {
              name: "id_number",
              label: langContent.labels.idNumber,
              placeholder: langContent.placeholders.idNumber,
            },
            {
              name: "district",
              label: langContent.labels.district,
              placeholder: langContent.placeholders.district,
            },
            {
              name: "name",
              label: langContent.labels.fullName,
              placeholder: langContent.placeholders.fullName,
            },
            {
              name: "municipality",
              label: langContent.labels.municipality,
              placeholder: langContent.placeholders.municipality,
            },
            {
              name: "dob",
              label: langContent.labels.dob,
              placeholder: langContent.placeholders.dob,
            },
            {
              name: "father_name",
              label: langContent.labels.fatherName,
              placeholder: langContent.placeholders.fatherName,
            },
            {
              name: "mother_name",
              label: langContent.labels.motherName,
              placeholder: langContent.placeholders.motherName,
            },
          ].map((field) => (
            <div key={field.name}>
              <label
                htmlFor={field.name}
                className="block text-gray-700 text-sm font-medium mb-2"
              >
                {field.label}
              </label>
              <input
                type="text"
                id={field.name}
                name={field.name}
                value={formData[field.name]}
                onChange={handleChange}
                placeholder={field.placeholder}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus-ring-green text-gray-800"
                required
              />
            </div>
          ))}
        </div>

        <div className="mt-8 mb-8">
          <label className="block text-gray-700 text-sm font-medium mb-2">
            {langContent.labels.genderLabel}
          </label>
          <div className="flex items-center space-x-6">
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio text-parrot-green focus-ring-green w-5 h-5"
                name="gender"
                value={langContent.labels.genderMaleText} 
                checked={formData.gender === langContent.labels.genderMaleText} 
                onChange={handleChange}
              />
              <span className="ml-2 text-gray-700">
                {langContent.labels.genderMaleText}
              </span>
            </label>
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio text-parrot-green focus-ring-green w-5 h-5"
                name="gender"
                value={langContent.labels.genderFemaleText} 
                checked={
                  formData.gender === langContent.labels.genderFemaleText
                } 
                onChange={handleChange}
              />
              <span className="ml-2 text-gray-700">
                {langContent.labels.genderFemaleText}
              </span>
            </label>
          </div>
        </div>

        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={onBack}
            className="px-8 py-3 rounded-full border-2 border-gray-400 text-gray-700 font-semibold text-lg shadow-md hover:bg-gray-100 transition-colors focus-ring-green"
          >
            {langContent.buttons.backBtn}
          </button>
          <button
            type="submit"
            disabled={isLoading}
            className="px-8 py-3 rounded-full parrot-green text-white font-semibold text-lg shadow-md hover:opacity-90 transition-opacity focus-ring-green disabled:opacity-50"
          >
            {isLoading ? "Correcting..." : langContent.buttons.correctBtn}
          </button>
        </div>
      </form>
    </div>
  );
}
