import React from "react";

export default function PlanResult({ plan }) {
  if (!plan) return null;

  return (
    <div className="plan-result">
      <h2>Your AI Fitness Plan 🧠</h2>

      {/* 📊 Macros Section */}
      <h3>📊 Macros</h3>
      {plan.macros ? (
        <div className="macros">
          <p>
            🔥 Calories: <strong>{plan.macros.calories}</strong>
          </p>
          <p>
            🍗 Protein: <strong>{plan.macros.protein_g} g</strong>
          </p>
          <p>
            🥑 Fat: <strong>{plan.macros.fat_g} g</strong>
          </p>
          <p>
            🍞 Carbs: <strong>{plan.macros.carbs_g} g</strong>
          </p>
        </div>
      ) : (
        <p>No macro data available.</p>
      )}

      {/* 🥗 Meal Plan */}
      <h3>🥗 7-Day Meal Plan</h3>
      {plan.meal_plan?.length > 0 ? (
        <div className="meal-plan">
          {plan.meal_plan.map((day, idx) => (
            <div key={idx} className="day-plan">
              <h4>Day {day.day}</h4>
              <ul>
                {day.meals?.map((meal, i) => (
                  <li key={i}>
                    🍽️ <strong>{meal.meal_time}:</strong> {meal.food}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ) : (
        <p>No meal plan generated.</p>
      )}

      {/* 🏋️ Workout Plan */}
      <h3>🏋️ 7-Day Workout Plan</h3>
      {plan.workout_plan?.length > 0 ? (
        <div className="workout-plan">
          {plan.workout_plan.map((day, idx) => (
            <div key={idx} className="day-plan">
              <h4>Day {day.day}</h4>
              <ul>
                {day.exercises?.map((ex, i) => (
                  <li key={i}>
                    🏃‍♂️ <strong>{ex.name}</strong> — {ex.sets} sets × {ex.reps}{" "}
                    reps
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ) : (
        <p>No workout plan generated.</p>
      )}

      {/* 📅 Duration */}
      <h3>📅 Duration</h3>
      <p>{plan.duration_weeks || 8} weeks</p>
    </div>
  );
}
