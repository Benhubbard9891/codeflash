"""
Command Line Interface for Codeflash
"""

import click
import sys
from pathlib import Path
from .optimizer import CodeOptimizer
from .cost_analyzer import CostAnalyzer
from .github_integration import GitHubPRGenerator


@click.group()
@click.version_option(version="0.1.0")
def main():
    """
    Codeflash - AI-Powered Python Performance Optimizer
    
    Automates code refactoring and optimization via GitHub Pull Requests.
    """
    pass


@main.command()
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--goal', type=click.Choice(['speed', 'cost', 'memory']), 
              default='speed', 
              help='Optimization goal: speed (default), cost, or memory')
@click.option('--create-pr', is_flag=True, 
              help='Create a GitHub Pull Request with the optimizations')
@click.option('--repo', type=str, 
              help='GitHub repository (format: owner/repo)')
@click.option('--token', type=str, envvar='GITHUB_TOKEN',
              help='GitHub token for PR creation (or set GITHUB_TOKEN env var)')
@click.option('--dry-run', is_flag=True,
              help='Show what would be optimized without making changes')
def optimize(path, goal, create_pr, repo, token, dry_run):
    """
    Optimize Python code in the specified path.
    
    Examples:
    
    \b
    # Optimize for speed (default)
    $ codeflash optimize ./src
    
    \b
    # Optimize for cloud cost reduction
    $ codeflash optimize ./src --goal=cost
    
    \b
    # Create a PR with optimizations
    $ codeflash optimize ./src --goal=cost --create-pr --repo=owner/repo
    """
    click.echo(f"🚀 Codeflash v0.1.0")
    click.echo(f"📂 Analyzing: {path}")
    click.echo(f"🎯 Goal: {goal}")
    
    if dry_run:
        click.echo("🔍 Dry run mode - no changes will be made")
    
    # Initialize the appropriate analyzer based on goal
    if goal == 'cost':
        analyzer = CostAnalyzer(path)
        click.echo("\n💰 Running Cloud Cost Optimization Analysis...")
    else:
        analyzer = CodeOptimizer(path, goal=goal)
        click.echo(f"\n⚡ Running {goal.capitalize()} Optimization Analysis...")
    
    # Analyze the code
    results = analyzer.analyze()
    
    if not results:
        click.echo("\n✅ No optimization opportunities found!")
        return
    
    # Display results
    click.echo(f"\n📊 Found {len(results)} optimization opportunities:")
    for i, result in enumerate(results, 1):
        click.echo(f"\n{i}. {result['file']}:{result['line']}")
        click.echo(f"   Issue: {result['issue']}")
        click.echo(f"   Impact: {result['impact']}")
        click.echo(f"   Suggestion: {result['suggestion']}")
    
    if dry_run:
        click.echo("\n🔍 Dry run complete. Use without --dry-run to apply changes.")
        return
    
    # Apply optimizations
    if click.confirm("\n🔧 Apply these optimizations?", default=True):
        click.echo("\n⚙️  Applying optimizations...")
        applied = analyzer.apply_optimizations(results)
        click.echo(f"✅ Applied {applied} optimizations")
        
        # Create PR if requested
        if create_pr:
            if not repo or not token:
                click.echo("❌ Error: --repo and --token are required for PR creation")
                sys.exit(1)
            
            click.echo(f"\n🔀 Creating Pull Request for {repo}...")
            pr_generator = GitHubPRGenerator(repo, token)
            pr_url = pr_generator.create_pr(results, goal)
            click.echo(f"✅ Pull Request created: {pr_url}")
    else:
        click.echo("❌ Optimizations cancelled")


@main.command()
@click.argument('file', type=click.Path(exists=True))
def analyze(file):
    """
    Analyze a single Python file and show optimization recommendations.
    
    This command provides detailed analysis without making any changes.
    """
    click.echo(f"🔍 Analyzing {file}...")
    
    analyzer = CostAnalyzer(file)
    results = analyzer.analyze()
    
    if not results:
        click.echo("✅ No issues found!")
        return
    
    click.echo(f"\n📊 Analysis Results:\n")
    for result in results:
        click.echo(f"Line {result['line']}: {result['issue']}")
        click.echo(f"  Impact: {result['impact']}")
        click.echo(f"  💡 {result['suggestion']}\n")


if __name__ == '__main__':
    main()
