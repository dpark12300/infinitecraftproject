import asyncio

from infinitecraft import InfiniteCraft


async def main():
    rate_limit_delay = 2  # seconds

    async with InfiniteCraft(api_rate_limit=30) as game:
        while True:
            # Get all discovered elements
            elements = game.discoveries

            # Iterate over all possible pairs of elements
            result = None
            novel = None

            for i, element in enumerate(elements):
                for _, element2 in enumerate(elements[i + 1:]):
                    first_element = element
                    second_element = element2

                    # Merge the elements and store the result
                    result = await game.merge(first_element, second_element)

                    # Check if the result is a first discovery
                    if result.is_first_discovery:
                        novel = "✅"
                    else:
                        novel = "❎"

                    # Print the combination and result
                    print(
                        f"{first_element} + {second_element} = {result} "
                        f"(New: {novel})"
                    )

                    # Apply rate limiting
                    await asyncio.sleep(rate_limit_delay)


if __name__ == "__main__":
    asyncio.run(main())
