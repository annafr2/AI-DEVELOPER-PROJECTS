"""
Main execution script for Logistic Regression project
Run this file to execute the complete analysis
"""

import os
import sys
import numpy as np
import pandas as pd

from logistic_regression import (
    LogisticRegression, 
    generate_synthetic_data, 
    create_results_table,
    print_summary_statistics
)
from visualizations import (
    plot_data_and_boundary,
    plot_predictions_comparison,
    plot_training_progress,
    plot_beta_evolution
)


def main():
    """Main execution function"""
    
    print("\n" + "="*70)
    print(f"{'Logistic Regression Project - Binary Classification':^70}")
    print("="*70 + "\n")
    
    # Create output directory
    output_dir = 'outputs'
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Generate synthetic dataset
    print("Step 1: Generating Synthetic Dataset")
    print("-" * 70)
    n_samples = 200
    X, y = generate_synthetic_data(n_samples=n_samples)
    
    print(f"✓ Created dataset with {len(X)} samples")
    print(f"  - Group 0 (Healthy): {np.sum(y == 0)} samples")
    print(f"  - Group 1 (Sick): {np.sum(y == 1)} samples")
    print(f"  - Number of features (including Bias): {X.shape[1]}\n")
    
    # Step 2: Train model
    print("Step 2: Training Model")
    print("-" * 70)
    model = LogisticRegression(learning_rate=0.1, n_iterations=1000)
    model.fit(X, y, verbose=True)
    
    # Step 3: Make predictions
    print("Step 3: Making Predictions")
    print("-" * 70)
    y_pred_proba = model.predict_proba(X)
    y_pred = model.predict(X)
    
    # Calculate accuracy
    accuracy = np.mean(y == y_pred)
    print(f"✓ Model accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)\n")
    
    # Step 4: Create results table
    print("Step 4: Creating Results Table")
    print("-" * 70)
    results_df = create_results_table(X, y, y_pred_proba)
    
    # Save to CSV
    csv_path = os.path.join(output_dir, 'results_table.csv')
    results_df.to_csv(csv_path, index=True, encoding='utf-8-sig')
    print(f"✓ Table saved to: {csv_path}")
    
    # Save to Excel
    excel_path = os.path.join(output_dir, 'results_table.xlsx')
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        results_df.to_excel(writer, sheet_name='Results', index=True)
    print(f"✓ Table saved to: {excel_path}")
    
    # Print statistics
    print_summary_statistics(results_df)
    
    # Step 5: Create visualizations
    print(f"\n{'='*70}")
    print("Step 5: Creating Visualizations")
    print("-" * 70)
    
    print("\n1. Decision boundary plot...")
    plot_data_and_boundary(X, y, model, 
                          save_path=os.path.join(output_dir, 'decision_boundary.png'))
    
    print("2. Predictions comparison plot...")
    plot_predictions_comparison(y, y_pred_proba,
                               save_path=os.path.join(output_dir, 'predictions_comparison.png'))
    
    print("3. Training progress plot...")
    plot_training_progress(model.likelihood_history, model.error_history,
                          save_path=os.path.join(output_dir, 'training_progress.png'))
    
    print("4. Beta evolution plot...")
    plot_beta_evolution(model.beta_history,
                       save_path=os.path.join(output_dir, 'beta_evolution.png'))
    
    # Step 6: Final summary
    print(f"\n{'='*70}")
    print(f"{'Final Summary':^70}")
    print("="*70)
    
    final_ll = model.likelihood_history[-1]
    final_mse = model.error_history[-1]
    
    print(f"\nTrained Parameters (Beta):")
    for i, beta_val in enumerate(model.beta):
        param_name = 'β0 (Bias)' if i == 0 else f'β{i}'
        print(f"  {param_name}: {beta_val:.6f}")
    
    print(f"\nPerformance Metrics:")
    print(f"  - Final Log-Likelihood: {final_ll:.4f}")
    print(f"  - Final Mean Squared Error: {final_mse:.6f}")
    print(f"  - Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    print(f"\nGenerated Files:")
    print(f"  ✓ {os.path.join(output_dir, 'results_table.csv')}")
    print(f"  ✓ {os.path.join(output_dir, 'results_table.xlsx')}")
    print(f"  ✓ {os.path.join(output_dir, 'decision_boundary.png')}")
    print(f"  ✓ {os.path.join(output_dir, 'predictions_comparison.png')}")
    print(f"  ✓ {os.path.join(output_dir, 'training_progress.png')}")
    print(f"  ✓ {os.path.join(output_dir, 'beta_evolution.png')}")
    
    print(f"\n{'='*70}")
    print(f"{'Project Completed Successfully! 🎉':^70}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()