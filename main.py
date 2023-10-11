from personalscrapers import scrape_socialdeal


def main():
    """Main function
    """
    df = scrape_socialdeal()
    df.to_html('socialdeal.html', index=False,
        border=1, justify='center', render_links=True, escape=False)

if __name__ == "__main__":
    main()
