# trunk-ignore-all(isort)
import asyncio
import random
import time
from collections import defaultdict

from aiohttp import ClientError
from infinitecraft import Element, InfiniteCraft

RATE_LIMIT_DELAY = 2  # seconds
RETRY_DELAY = 10  # seconds


async def main():
    async with InfiniteCraft() as game:
        # Track discoveries per element
        discovery_counts = defaultdict(int)
        # New dictionary to track successful novel discoveries
        novel_discovery_counts = defaultdict(int)
        novel_elements = []  # List to store novel elements

        while True:
            elements = game.discoveries

            # Prioritize elements involved in fewer successful novel discoveries
            candidates = sorted(
                elements,
                key=lambda e: (
                    novel_discovery_counts[e.name], discovery_counts[e.name], random.random()),
            )

            for i in range(len(candidates)):
                for j in range(i + 1, len(candidates)):
                    first_element = candidates[i]
                    second_element = candidates[j]

                    try:
                        # Pair the elements and store the result
                        result = await game.pair(first_element, second_element)
                    except ClientError:
                        print("Internet issue occurred. Retrying in a few seconds...")
                        await asyncio.sleep(RETRY_DELAY)
                        continue

                    # Check if the result is novel
                    novel = result.is_first_discovery

                    # Print the combination and result
                    print(
                        f"Combining {first_element} and {second_element} resulted in {result} (Novel: {
                            novel})"
                    )

                    # Update discovery counts
                    discovery_counts[first_element.name] += 1
                    discovery_counts[second_element.name] += 1
                    if novel:
                        discovery_counts[result.name] += 1
                        # Add novel result to the list
                        novel_elements.append(result)
                        # Update novel discovery counts
                        novel_discovery_counts[first_element.name] += 1
                        novel_discovery_counts[second_element.name] += 1

                    # Apply rate limiting
                    await asyncio.sleep(RATE_LIMIT_DELAY)

            # Now pair novel elements together
            for i in range(len(novel_elements)):
                for j in range(i + 1, len(novel_elements)):
                    first_element = novel_elements[i]
                    second_element = novel_elements[j]

                    try:
                        # Pair the elements and store the result
                        result = await game.pair(first_element, second_element)
                    except ClientError:
                        print("Internet issue occurred. Retrying in a few seconds...")
                        await asyncio.sleep(RETRY_DELAY)
                        continue

                    # Check if the result is novel
                    novel = result.is_first_discovery

                    # Print the combination and result
                    print(
                        f"Combining {first_element} and {second_element} resulted in {result} (Novel: {
                            novel})"
                    )

                    # Update discovery counts
                    if novel:
                        discovery_counts[result.name] += 1
                        # Add novel result to the list
                        novel_elements.append(result)
                        # Update novel discovery counts
                        novel_discovery_counts[first_element.name] += 1
                        novel_discovery_counts[second_element.name] += 1

                    # Apply rate limiting
                    await asyncio.sleep(RATE_LIMIT_DELAY)

if __name__ == "__main__":
    asyncio.run(main())
