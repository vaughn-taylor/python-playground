import pkg_resources
import subprocess

def get_outdated_packages():
    result = subprocess.run(['pip', 'list', '--outdated', '--format=freeze'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    outdated = []

    for line in lines:
        if '==' in line:
            pkg_name = line.split('==')[0]
            try:
                dist = pkg_resources.get_distribution(pkg_name)
                current_version = dist.version
                # Extract latest version from line if possible
                latest_version = line.split('->')[-1].strip() if '->' in line else 'unknown'
                outdated.append((pkg_name, current_version, latest_version))
            except pkg_resources.DistributionNotFound:
                pass

    return outdated

def print_report(outdated):
    if not outdated:
        print("🎉 All packages are up to date!")
        return

    print("📦 Outdated packages:")
    for name, current, latest in outdated:
        print(f" - {name}: {current} → {latest}")

if __name__ == "__main__":
    outdated_packages = get_outdated_packages()
    print_report(outdated_packages)
