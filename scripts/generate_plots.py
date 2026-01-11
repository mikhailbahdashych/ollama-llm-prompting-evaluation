#!/usr/bin/env python3
"""Generate visualization plots from evaluation CSV report.

This script creates multiple plots to analyze LLM performance across
tasks, models, and prompting strategies.

Usage:
    python scripts/generate_plots.py <csv_file_path>
    python scripts/generate_plots.py data/results/reports/run_2026-01-11_15-30-45_results.csv

    Or use --latest to process the most recent report:
    python scripts/generate_plots.py --latest
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from rich.console import Console

console = Console()

# Set style for better-looking plots
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['figure.dpi'] = 100


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate visualization plots from evaluation CSV report"
    )

    parser.add_argument(
        "csv_path",
        nargs="?",
        type=Path,
        help="Path to CSV file (e.g., data/results/reports/run_xxx_results.csv)"
    )

    parser.add_argument(
        "--latest",
        action="store_true",
        help="Use the most recent CSV report"
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory to save plots (default: same directory as CSV with _plots suffix)"
    )

    parser.add_argument(
        "--format",
        type=str,
        default="png",
        choices=["png", "pdf", "svg"],
        help="Output format for plots (default: png)"
    )

    return parser.parse_args()


def find_latest_csv(reports_dir: Path = Path("data/results/reports")) -> Path:
    """Find the most recent CSV report.

    Args:
        reports_dir: Directory containing reports

    Returns:
        Path to the latest CSV file

    Raises:
        FileNotFoundError: If no CSV files found
    """
    if not reports_dir.exists():
        raise FileNotFoundError(f"Reports directory not found: {reports_dir}")

    csv_files = list(reports_dir.glob("*_results.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {reports_dir}")

    latest = max(csv_files, key=lambda p: p.stat().st_mtime)
    return latest


def load_and_prepare_data(csv_path: Path) -> pd.DataFrame:
    """Load CSV and prepare data for plotting.

    Args:
        csv_path: Path to CSV file

    Returns:
        Prepared DataFrame
    """
    df = pd.read_csv(csv_path)

    # Filter out results without scores
    df_scored = df[df['total_score'].notna()].copy()

    if df_scored.empty:
        raise ValueError("No scored results found in CSV. Please score the results first.")

    # Clean up model names for display
    df_scored['model_display'] = df_scored['model_name'].str.replace(':', ' ').str.replace('_', ' ')

    # Parse scores dict if it's stored as string
    if df_scored['scores'].dtype == 'object':
        try:
            df_scored['scores_dict'] = df_scored['scores'].apply(
                lambda x: json.loads(x.replace("'", '"')) if pd.notna(x) and isinstance(x, str) else {}
            )
        except:
            df_scored['scores_dict'] = None

    return df_scored


def plot_total_score_by_model(df: pd.DataFrame, output_path: Path):
    """Plot average total score by model.

    Args:
        df: DataFrame with results
        output_path: Path to save the plot
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Calculate average score per model
    model_scores = df.groupby('model_display')['total_score'].agg(['mean', 'std']).reset_index()
    model_scores = model_scores.sort_values('mean', ascending=False)

    # Create bar plot
    bars = ax.bar(
        model_scores['model_display'],
        model_scores['mean'],
        yerr=model_scores['std'],
        capsize=5,
        alpha=0.8,
        edgecolor='black'
    )

    # Color bars
    colors = sns.color_palette("husl", len(bars))
    for bar, color in zip(bars, colors):
        bar.set_color(color)

    ax.set_xlabel('Model', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Total Score', fontsize=12, fontweight='bold')
    ax.set_title('Average Performance by Model', fontsize=14, fontweight='bold', pad=20)
    ax.tick_params(axis='x', rotation=45)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            f'{height:.1f}',
            ha='center',
            va='bottom',
            fontweight='bold'
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    console.print(f"[green]Saved:[/green] {output_path.name}")


def plot_performance_by_task(df: pd.DataFrame, output_path: Path):
    """Plot performance by task for each model.

    Args:
        df: DataFrame with results
        output_path: Path to save the plot
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    # Calculate average score per model per task
    task_scores = df.groupby(['task_id', 'model_display'])['total_score'].mean().reset_index()

    # Create grouped bar chart
    sns.barplot(
        data=task_scores,
        x='task_id',
        y='total_score',
        hue='model_display',
        ax=ax,
        palette='Set2'
    )

    ax.set_xlabel('Task', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Score', fontsize=12, fontweight='bold')
    ax.set_title('Performance by Task (Comparing Models)', fontsize=14, fontweight='bold', pad=20)
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Model', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    console.print(f"[green]Saved:[/green] {output_path.name}")


def plot_performance_by_strategy(df: pd.DataFrame, output_path: Path):
    """Plot performance by prompting strategy for each model.

    Args:
        df: DataFrame with results
        output_path: Path to save the plot
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Calculate average score per model per strategy
    strategy_scores = df.groupby(['strategy', 'model_display'])['total_score'].mean().reset_index()

    # Create grouped bar chart
    sns.barplot(
        data=strategy_scores,
        x='strategy',
        y='total_score',
        hue='model_display',
        ax=ax,
        palette='Set1'
    )

    ax.set_xlabel('Prompting Strategy', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Score', fontsize=12, fontweight='bold')
    ax.set_title('Performance by Prompting Strategy', fontsize=14, fontweight='bold', pad=20)
    ax.legend(title='Model', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    console.print(f"[green]Saved:[/green] {output_path.name}")


def plot_heatmap(df: pd.DataFrame, output_path: Path):
    """Plot heatmap of model vs task performance.

    Args:
        df: DataFrame with results
        output_path: Path to save the plot
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create pivot table
    pivot = df.pivot_table(
        values='total_score',
        index='model_display',
        columns='task_id',
        aggfunc='mean'
    )

    # Create heatmap
    sns.heatmap(
        pivot,
        annot=True,
        fmt='.1f',
        cmap='YlOrRd',
        cbar_kws={'label': 'Average Score'},
        ax=ax,
        linewidths=0.5
    )

    ax.set_xlabel('Task', fontsize=12, fontweight='bold')
    ax.set_ylabel('Model', fontsize=12, fontweight='bold')
    ax.set_title('Performance Heatmap: Model × Task', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    console.print(f"[green]Saved:[/green] {output_path.name}")


def plot_score_distribution(df: pd.DataFrame, output_path: Path):
    """Plot score distribution by model using box plots.

    Args:
        df: DataFrame with results
        output_path: Path to save the plot
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create box plot
    sns.boxplot(
        data=df,
        x='model_display',
        y='total_score',
        ax=ax,
        hue='model_display',
        palette='pastel',
        legend=False
    )

    # Overlay individual points
    sns.swarmplot(
        data=df,
        x='model_display',
        y='total_score',
        ax=ax,
        color='black',
        alpha=0.5,
        size=3
    )

    ax.set_xlabel('Model', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Score', fontsize=12, fontweight='bold')
    ax.set_title('Score Distribution by Model', fontsize=14, fontweight='bold', pad=20)
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    console.print(f"[green]Saved:[/green] {output_path.name}")


def plot_generation_time(df: pd.DataFrame, output_path: Path):
    """Plot generation time comparison.

    Args:
        df: DataFrame with results
        output_path: Path to save the plot
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Convert ms to seconds
    df_plot = df.copy()
    df_plot['generation_time_sec'] = df_plot['generation_time_ms'] / 1000

    # Calculate average generation time per model
    time_stats = df_plot.groupby('model_display')['generation_time_sec'].agg(['mean', 'std']).reset_index()
    time_stats = time_stats.sort_values('mean', ascending=False)

    # Create bar plot
    bars = ax.bar(
        time_stats['model_display'],
        time_stats['mean'],
        yerr=time_stats['std'],
        capsize=5,
        alpha=0.8,
        edgecolor='black',
        color='skyblue'
    )

    ax.set_xlabel('Model', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Generation Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Average Generation Time by Model', fontsize=14, fontweight='bold', pad=20)
    ax.tick_params(axis='x', rotation=45)

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            f'{height:.1f}s',
            ha='center',
            va='bottom',
            fontweight='bold'
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    console.print(f"[green]Saved:[/green] {output_path.name}")


def plot_criteria_breakdown(df: pd.DataFrame, output_path: Path):
    """Plot breakdown of scores by evaluation criteria.

    Args:
        df: DataFrame with results
        output_path: Path to save the plot
    """
    if 'scores_dict' not in df.columns or df['scores_dict'].isna().all():
        console.print("[yellow]Skipping criteria breakdown: scores not parsed as dict[/yellow]")
        return

    # Extract all criteria scores
    criteria_data = []
    for _, row in df.iterrows():
        if isinstance(row['scores_dict'], dict):
            for criterion, score in row['scores_dict'].items():
                criteria_data.append({
                    'model': row['model_display'],
                    'criterion': criterion,
                    'score': score
                })

    if not criteria_data:
        console.print("[yellow]Skipping criteria breakdown: no criteria data found[/yellow]")
        return

    criteria_df = pd.DataFrame(criteria_data)

    # Get unique criteria
    criteria_list = criteria_df['criterion'].unique()
    n_criteria = len(criteria_list)

    # Create subplots
    fig, axes = plt.subplots(
        nrows=(n_criteria + 1) // 2,
        ncols=2,
        figsize=(14, 4 * ((n_criteria + 1) // 2))
    )
    axes = axes.flatten() if n_criteria > 1 else [axes]

    for idx, criterion in enumerate(criteria_list):
        criterion_data = criteria_df[criteria_df['criterion'] == criterion]

        sns.barplot(
            data=criterion_data,
            x='model',
            y='score',
            ax=axes[idx],
            hue='model',
            palette='viridis',
            errorbar='sd',
            legend=False
        )

        axes[idx].set_title(f'{criterion.replace("_", " ").title()}', fontweight='bold')
        axes[idx].set_xlabel('Model', fontweight='bold')
        axes[idx].set_ylabel('Score', fontweight='bold')
        axes[idx].tick_params(axis='x', rotation=45)

    # Hide unused subplots
    for idx in range(n_criteria, len(axes)):
        axes[idx].set_visible(False)

    plt.suptitle('Performance Breakdown by Evaluation Criteria', fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    console.print(f"[green]Saved:[/green] {output_path.name}")


def plot_radar_chart(df: pd.DataFrame, output_path: Path):
    """Plot radar/spider chart showing model performance across tasks.

    Args:
        df: DataFrame with results
        output_path: Path to save the plot
    """
    import numpy as np

    # Calculate average score per model per task
    task_scores = df.groupby(['task_id', 'model_display'])['total_score'].mean().reset_index()

    # Get unique tasks and models
    tasks = sorted(task_scores['task_id'].unique())
    models = sorted(task_scores['model_display'].unique())

    if len(tasks) < 3:
        console.print("[yellow]Skipping radar chart: need at least 3 tasks for meaningful visualization[/yellow]")
        return

    # Number of variables
    num_vars = len(tasks)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

    # Plot each model
    colors = sns.color_palette("husl", len(models))

    for idx, model in enumerate(models):
        model_data = task_scores[task_scores['model_display'] == model]

        # Get scores in order of tasks
        values = []
        for task in tasks:
            task_row = model_data[model_data['task_id'] == task]
            if not task_row.empty:
                values.append(task_row['total_score'].values[0])
            else:
                values.append(0)

        # Complete the circle
        values += values[:1]

        # Plot
        ax.plot(angles, values, 'o-', linewidth=2, label=model, color=colors[idx])
        ax.fill(angles, values, alpha=0.15, color=colors[idx])

    # Set labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([t.replace('_', '\n') for t in tasks], size=9)
    ax.set_ylim(0, None)
    ax.set_title('Model Performance Across Tasks\n(Radar Chart)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    console.print(f"[green]Saved:[/green] {output_path.name}")


def plot_task_winner_comparison(df: pd.DataFrame, output_path: Path):
    """Plot showing which model wins for each task.

    Args:
        df: DataFrame with results
        output_path: Path to save the plot
    """
    # Calculate average score per model per task
    task_scores = df.groupby(['task_id', 'model_display'])['total_score'].mean().reset_index()

    # Find winner for each task
    tasks = sorted(task_scores['task_id'].unique())
    models = sorted(task_scores['model_display'].unique())

    # Calculate subplot layout
    n_tasks = len(tasks)
    ncols = min(3, n_tasks)
    nrows = (n_tasks + ncols - 1) // ncols

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(5 * ncols, 5 * nrows)
    )

    # Ensure axes is always a flat array
    if n_tasks == 1:
        axes = [axes]
    elif nrows == 1:
        axes = list(axes)
    else:
        axes = axes.flatten()

    for idx, task in enumerate(tasks):
        task_data = task_scores[task_scores['task_id'] == task].sort_values('total_score', ascending=False)

        # Create bar plot
        bars = axes[idx].barh(
            task_data['model_display'],
            task_data['total_score'],
            color=sns.color_palette("RdYlGn", len(task_data))[::-1]
        )

        # Highlight the winner
        bars[0].set_edgecolor('black')
        bars[0].set_linewidth(3)

        # Add value labels
        for bar in bars:
            width = bar.get_width()
            axes[idx].text(
                width,
                bar.get_y() + bar.get_height() / 2,
                f' {width:.1f}',
                ha='left',
                va='center',
                fontweight='bold'
            )

        axes[idx].set_title(
            f'{task.replace("_", " ").title()}\nWinner: {task_data.iloc[0]["model_display"]}',
            fontweight='bold',
            fontsize=10
        )
        axes[idx].set_xlabel('Score', fontweight='bold')
        axes[idx].invert_yaxis()

    # Hide unused subplots
    for idx in range(len(tasks), len(axes)):
        axes[idx].set_visible(False)

    plt.suptitle('Task-by-Task Winner Analysis', fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    console.print(f"[green]Saved:[/green] {output_path.name}")


def plot_model_specialization(df: pd.DataFrame, output_path: Path):
    """Plot showing relative performance (how much better/worse than average).

    Args:
        df: DataFrame with results
        output_path: Path to save the plot
    """
    # Calculate average score per model per task
    task_scores = df.groupby(['task_id', 'model_display'])['total_score'].mean().reset_index()

    # Calculate overall average for each task
    task_avg = df.groupby('task_id')['total_score'].mean()

    # Calculate relative performance (difference from task average)
    task_scores['relative_score'] = task_scores.apply(
        lambda row: row['total_score'] - task_avg[row['task_id']],
        axis=1
    )

    # Create pivot table
    pivot = task_scores.pivot(
        index='model_display',
        columns='task_id',
        values='relative_score'
    )

    fig, ax = plt.subplots(figsize=(14, 8))

    # Create heatmap
    sns.heatmap(
        pivot,
        annot=True,
        fmt='.1f',
        cmap='RdYlGn',
        center=0,
        cbar_kws={'label': 'Score vs Task Average'},
        ax=ax,
        linewidths=0.5
    )

    ax.set_xlabel('Task', fontsize=12, fontweight='bold')
    ax.set_ylabel('Model', fontsize=12, fontweight='bold')
    ax.set_title(
        'Model Specialization Heatmap\n(Positive = Better than average, Negative = Worse than average)',
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    console.print(f"[green]Saved:[/green] {output_path.name}")


def main():
    """Main entry point."""
    args = parse_args()

    # Determine CSV path
    if args.latest:
        try:
            csv_path = find_latest_csv()
            console.print(f"[cyan]Using latest CSV:[/cyan] {csv_path}\n")
        except FileNotFoundError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            return 1
    elif args.csv_path:
        csv_path = args.csv_path
        if not csv_path.exists():
            console.print(f"[bold red]Error:[/bold red] CSV file not found: {csv_path}")
            return 1
    else:
        console.print("[bold red]Error:[/bold red] Please provide csv_path or use --latest")
        return 1

    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        # Create plots directory next to CSV
        output_dir = csv_path.parent / f"{csv_path.stem}_plots"

    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"[bold cyan]Loading data from:[/bold cyan] {csv_path}")

    # Load and prepare data
    try:
        df = load_and_prepare_data(csv_path)
    except Exception as e:
        console.print(f"[bold red]Error loading data:[/bold red] {e}")
        return 1

    console.print(f"[green]Loaded {len(df)} scored results[/green]\n")

    # Generate plots
    console.print("[bold cyan]Generating plots...[/bold cyan]\n")

    ext = args.format

    plot_total_score_by_model(df, output_dir / f"1_total_score_by_model.{ext}")
    plot_performance_by_task(df, output_dir / f"2_performance_by_task.{ext}")
    plot_performance_by_strategy(df, output_dir / f"3_performance_by_strategy.{ext}")
    plot_heatmap(df, output_dir / f"4_heatmap_model_task.{ext}")
    plot_score_distribution(df, output_dir / f"5_score_distribution.{ext}")
    plot_generation_time(df, output_dir / f"6_generation_time.{ext}")
    plot_criteria_breakdown(df, output_dir / f"7_criteria_breakdown.{ext}")

    # New task-focused plots
    plot_radar_chart(df, output_dir / f"8_radar_chart_tasks.{ext}")
    plot_task_winner_comparison(df, output_dir / f"9_task_winners.{ext}")
    plot_model_specialization(df, output_dir / f"10_model_specialization.{ext}")

    console.print(f"\n[bold green]All plots generated successfully![/bold green]")
    console.print(f"[cyan]Plots saved to:[/cyan] {output_dir}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
