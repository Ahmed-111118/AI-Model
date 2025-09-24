import React, { useState } from "react";
import axios from "axios";

export default function PlanForm({ setPlan }) {
  const [age, setAge] = useState("");
  const [height, setHeight] = useState(""); // in feet
  const [weight, setWeight] = useState("");
  const [gender, setGender] = useState("male");
  const [activityLevel, setActivityLevel] = useState("moderate");
  const [goal, setGoal] = useState("maintain");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // ✅ Basic frontend validation before calling API
    if (
      !age ||
      !height ||
      !weight ||
      isNaN(age) ||
      isNaN(height) ||
      isNaN(weight)
    ) {
      alert("Please enter valid age, height, and weight.");
      return;
    }

    // ✅ Convert ft → cm
    const height_cm = parseFloat(height) * 30.48;

    // ✅ Extra safety checks before API call
    if (height_cm < 50 || height_cm > 250) {
      alert("Height must be between 50 cm and 250 cm.");
      return;
    }
    if (weight < 20 || weight > 300) {
      alert("Weight must be between 20 kg and 300 kg.");
      return;
    }
    if (age < 10 || age > 100) {
      alert("Age must be between 10 and 100.");
      return;
    }

    setLoading(true);

    try {
      const res = await axios.get("http://127.0.0.1:8000/generate", {
        params: {
          age: parseInt(age),
          height_cm: height_cm,
          weight_kg: parseFloat(weight),
          gender,
          activity_level: activityLevel,
          goal, // ✅ values now exactly match backend validation
        },
      });

      setPlan(res.data.plan);
    } catch (err) {
      console.error("Error fetching plan:", err);
      alert(
        err.response?.data?.detail ||
          "Something went wrong. Please check your inputs or backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="plan-form" onSubmit={handleSubmit}>
      <label>Age:</label>
      <input
        type="number"
        value={age}
        onChange={(e) => setAge(e.target.value)}
        required
      />

      <label>Height (ft):</label>
      <input
        type="number"
        value={height}
        onChange={(e) => setHeight(e.target.value)}
        required
      />

      <label>Weight (kg):</label>
      <input
        type="number"
        value={weight}
        onChange={(e) => setWeight(e.target.value)}
        required
      />

      <label>Gender:</label>
      <select value={gender} onChange={(e) => setGender(e.target.value)}>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
      </select>

      <label>Activity Level:</label>
      <select
        value={activityLevel}
        onChange={(e) => setActivityLevel(e.target.value)}
      >
        <option value="sedentary">Sedentary</option>
        <option value="light">Light</option>
        <option value="moderate">Moderate</option>
        <option value="active">Active</option>
        <option value="very_active">Very Active</option>
      </select>

      <label>Goal:</label>
      <select value={goal} onChange={(e) => setGoal(e.target.value)}>
        <option value="lose">Lose Weight</option>
        <option value="gain">Gain Muscle</option>
        <option value="maintain">Maintain Weight</option>
      </select>

      <button type="submit" disabled={loading}>
        {loading ? "Generating..." : "Generate Plan"}
      </button>
    </form>
  );
}
