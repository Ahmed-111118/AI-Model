// src/components/PlanDisplay.jsx
import React from "react";

export default function PlanDisplay({ plan }) {
  if (!plan) return null;
  console.log("📦 Full plan object:", plan);
  console.log("🍽️ Meal plan data:", plan.meal_plan);
  console.log("🏋️‍♂️ Workout plan data:", plan.workout_plan);

  return (
    <div className="plan-display">
      <h2>🏋️‍♂️ Your Personalized Plan</h2>

      <div className="macros">
        <h3>Daily Nutrition</h3>
        <p>
          <strong>Calories:</strong> {plan.calories}
        </p>
        <p>
          <strong>Protein:</strong> {plan.protein || plan.protein_g} g
        </p>
        <p>
          <strong>Fat:</strong> {plan.fat || plan.fat_g} g
        </p>
        <p>
          <strong>Carbs:</strong> {plan.carbs || plan.carbs_g} g
        </p>
      </div>

      {/* ✅ Diet Plan */}
      {plan.meal_plan && (
        <div className="meal-plan">
          <h3>🍽️ Meal Plan</h3>
          {Array.isArray(plan.meal_plan) ? (
            <div>
              {plan.meal_plan.map((meal, index) => (
                <div key={index} className="meal">
                  <h4>{meal.meal || `Meal ${index + 1}`}</h4>
                  {Array.isArray(meal.items) ? (
                    <ul>
                      {meal.items.map((item, idx) => (
                        <li key={idx}>{item}</li>
                      ))}
                    </ul>
                  ) : (
                    <p>{meal.items || meal.description || meal}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p>{plan.meal_plan}</p>
          )}
        </div>
      )}

      {/* ✅ Workout Plan */}
      {plan.workout_plan && (
        <div className="workout-plan">
          <h3>🏋️‍♂️ Workout Plan</h3>
          {Array.isArray(plan.workout_plan) ? (
            <div>
              {plan.workout_plan.map((workout, index) => (
                <div key={index} className="workout-day">
                  <h4>{workout.day || `Workout ${index + 1}`}</h4>
                  {Array.isArray(workout.exercises) ? (
                    <ul>
                      {workout.exercises.map((exercise, idx) => (
                        <li key={idx}>{exercise}</li>
                      ))}
                    </ul>
                  ) : (
                    <p>{workout.exercises || workout}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p>{plan.workout_plan}</p>
          )}
        </div>
      )}
    </div>
  );
}
