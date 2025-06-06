import json
import decimal
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

DATA_BRANCH = 'python-coverage-comment-action-data'


def read_current_coverage(xml_path: Path) -> decimal.Decimal:
    root = ET.parse(xml_path).getroot()
    return decimal.Decimal(root.get('line-rate')) * 100


def read_previous_coverage(temp: Path) -> decimal.Decimal | None:
    if temp.exists():
        try:
            data = json.loads(temp.read_text())
            return decimal.Decimal(data['message'].rstrip('%'))
        except Exception:
            pass
    return None


def save_badge(path: Path, label: str, message: str, color: str):
    path.write_text(json.dumps({'schemaVersion':1,'label':label,'message':message,'color':color}))


def badge_color(rate: decimal.Decimal) -> str:
    if rate >= 100:
        return 'brightgreen'
    if rate >= 70:
        return 'orange'
    return 'red'


def evolution_color(delta: decimal.Decimal) -> str:
    if delta == 0:
        return 'blue'
    return 'brightgreen' if delta > 0 else 'red'


def main():
    cov = read_current_coverage(Path('coverage.xml'))

    subprocess.run(['git','fetch','origin',DATA_BRANCH],check=True)
    prev_file = Path('prev_endpoint.json')
    subprocess.run(['git','show',f'origin/{DATA_BRANCH}:endpoint.json'],check=True,stdout=prev_file.open('wb'))
    prev = read_previous_coverage(prev_file)

    if prev is not None:
        delta = cov - prev
        message = f'{int(prev)}% > {int(cov)}%'
    else:
        delta = decimal.Decimal('0')
        message = f'{int(cov)}%'
    save_badge(Path('evolution_endpoint.json'),'Coverage evolution',message,evolution_color(delta))

    subprocess.run(['diff-cover','coverage.xml',f'--compare-branch=origin/main','--json-report','pr_diff.json'],check=True)
    pr_cov = decimal.Decimal(json.loads(Path('pr_diff.json').read_text())['coverage'])
    save_badge(Path('pr_endpoint.json'),'PR Coverage',f'{int(pr_cov)}%',badge_color(pr_cov))

if __name__=='__main__':
    main()
