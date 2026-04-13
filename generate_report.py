# generate_report.py
import yfinance as yf
import pandas as pd
from datetime import datetime

def main():
    # 可自定义股票代码
    tickers = ['000001.SS', 'AAPL', 'TSLA']
    data = {}

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='5d')
            if not hist.empty:
                latest = hist.iloc[-1]
                data[ticker] = {
                    'Date': latest.name.strftime('%Y-%m-%d'),
                    'Close': round(latest['Close'], 2),
                    'Volume': int(latest['Volume'])
                }
        except Exception as e:
            data[ticker] = {'Error': str(e)}

    # 生成 Markdown 报告
    report_lines = [
        "# Daily Stock Report",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Beijing Time)\n",
        "| Ticker | Date | Close | Volume |",
        "|--------|------|-------|--------|"
    ]

    for ticker, info in data.items():
        if 'Error' not in info:
            report_lines.append(
                f"| {ticker} | {info['Date']} | {info['Close']} | {info['Volume']:,} |"
            )
        else:
            report_lines.append(
                f"| {ticker} | Error | {info['Error']} | - |"
            )

    with open('report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

if __name__ == '__main__':
    main()
