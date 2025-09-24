import React from "react";

export default function PlanDisplay({ plan }) {
  if (!plan) return null;

  const { macros, meal_plan, workout_plan } = plan;

  return (
    <div className="plan-result">
      <h2>Nutrition Plan</h2>
      <p>
        <strong>Calories:</strong> {macros.calories}
      </p>
      <p>
        <strong>Protein:</strong> {macros.protein_g} g
      </p>
      <p>
        <strong>Fats:</strong> {macros.fat_g} g
      </p>
      <p>
        <strong>Carbs:</strong> {macros.carbs_g} g
      </p>

      <h3>🍽 Meal Plan</h3>
      {plan?.meal_plan?.length > 0 ? (
        plan.meal_plan.map((dayPlan, index) => (
          <div key={index}>
            <h4>{dayPlan.day}</h4>
            <ul>
              {dayPlan.meals.map((meal, i) => (
                <li key={i}>{meal}</li>
              ))}
            </ul>
          </div>
        ))
      ) : (
        <p>No meal plan generated.</p>
      )}
      <h3>🏋️ Workout Plan</h3>
      {plan?.workout_plan?.length > 0 ? (
        plan.workout_plan.map((day, index) => (
          <div key={index}>
            <h4>{day.day}</h4>
            <ul>
              {day.exercises.map((exercise, i) => (
                <li key={i}>{exercise}</li>
              ))}
            </ul>
          </div>
        ))
      ) : (
        <p>No workout plan generated.</p>
      )}
    </div>
  );
}
