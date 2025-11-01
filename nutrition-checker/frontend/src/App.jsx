import React, { useState } from "react";
import FoodInputForm from "./components/FoodInputForm";
import ResultChart from "./components/ResultChart";
import { calculateBalance, getComment } from "./utils/api";

function App() {
  const [result, setResult] = useState(null);
  const [comment, setComment] = useState("");

  const handleSubmit = async (inputData) => {
    const res = await calculateBalance(inputData);
    setResult(res.result);
    const ai = await getComment(res.result);
    setComment(ai.comment);
  };

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-center">
        食品構成チェックアプリ
      </h1>
      <FoodInputForm onSubmit={handleSubmit} />
      {result && (
        <>
          <ResultChart data={result} />
          <p className="mt-4 text-lg text-center">{comment}</p>
        </>
      )}
    </div>
  );
}

export default App;
