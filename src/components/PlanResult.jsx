import React from "react";

export default function PlanResult({ plan }) {
  return (
    <div className="plan-result">
      <h2>Your AI Fitness Plan 🧠</h2>

      <h3>📊 Macros</h3>
      <p>Calories: {plan.macros?.calories}</p>
      <p>Protein: {plan.macros?.protein_g} g</p>
      <p>Fat: {plan.macros?.fat_g} g</p>
      <p>Carbs: {plan.macros?.carbs_g} g</p>

      <h3>🥗 Meal Plan</h3>
      {plan.meal_plan?.length > 0 ? (
        <ul>
          {plan.meal_plan.map((meal, idx) => (
            <li key={idx}>{meal}</li>
          ))}
        </ul>
      ) : (
        <p>No meal plan generated.</p>
      )}

      <h3>🏋️ Workout Plan</h3>
      {plan.workout_plan?.length > 0 ? (
        <ul>
          {plan.workout_plan.map((workout, idx) => (
            <li key={idx}>{workout}</li>
          ))}
        </ul>
      ) : (
        <p>No workout plan generated.</p>
      )}

      <h3>📅 Duration</h3>
      <p>{plan.duration_weeks} weeks</p>
    </div>
  );
}
