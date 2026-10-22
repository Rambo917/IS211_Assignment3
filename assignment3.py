
import argparse
import urllib.request
import csv
import re
from io import StringIO
from datetime import datetime
from collections import Counter


def downloadData(url):
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    return data


def processData(csvData):
    reader = csv.reader(StringIO(csvData))
    records = []

    for row in reader:
        if len(row) == 5:
            records.append(row)

    return records


def imageRequests(records):
    totalRequests = len(records)
    imageCount = 0

    for row in records:
        filePath = row[0].strip()

        if re.search(r"\.(jpg|gif|png)$", filePath, re.IGNORECASE):
            imageCount += 1

    if totalRequests > 0:
        percentage = (imageCount / totalRequests) * 100
    else:
        percentage = 0

    print(f"Image requests account for {percentage:.1f}% of all requests")


def popularBrowser(records):
    browsers = Counter()

    for row in records:
        userAgent = row[2]

        if re.search(r"Firefox", userAgent, re.IGNORECASE):
            browsers["Firefox"] += 1
        elif re.search(r"Chrome", userAgent, re.IGNORECASE):
            browsers["Chrome"] += 1
        elif re.search(r"MSIE|Trident", userAgent, re.IGNORECASE):
            browsers["Internet Explorer"] += 1
        elif re.search(r"Safari", userAgent, re.IGNORECASE):
            browsers["Safari"] += 1

    if browsers:
        browser, count = browsers.most_common(1)[0]
        print(f"The most popular browser is {browser} with {count} hits")
    else:
        print("No recognized browsers found")



def hourlyHits(records):
    hours = Counter({hour: 0 for hour in range(24)})

    for row in records:
        dateText = row[1].strip()

        for dateFormat in (
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y %I:%M:%S %p",
            "%Y-%m-%d %H:%M:%S"
        ):
            try:
                accessTime = datetime.strptime(dateText, dateFormat)
                hours[accessTime.hour] += 1
                break
            except ValueError:
                continue

    print("\nHits by hour:")
    for hour, count in sorted(
        hours.items(), key=lambda item: (-item[1], item[0])
    ):
        print(f"Hour {hour:02d} has {count} hits")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    records = processData(csvData)

    imageRequests(records)
    popularBrowser(records)
    hourlyHits(records)


if __name__ == "__main__":
    main()
