from bs4 import BeautifulSoup
import argparse
import html


def extract_code_tags(html_file, links_file):
    with open(html_file, "r") as input_file:
        html_content = input_file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <code> tags in the HTML
    code_tags = soup.find_all("code")

    final_html = f"""<html>
        <head>
        <script src="https://cdn.tailwindcss.com">
        </script>
        <style>
    .hidden {{
      display: none;
    }}
  </style>
        </head>
        <body>"""

    # Loop through the <code> tags and save them as separate HTML files
    for i, code_tag in enumerate(code_tags):
        decoded_html = html.unescape(code_tag.get_text())
        new_extracted_html = f"""
          <div class="flex-col m-4 justify-center rounded-md">
            <div class="flex justify-center">
              <button class="bg-blue-500 mb-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                onclick="toggleSections('group{i+1}')">Component {i+1}
              </button>
            </div>
            <div class="border rounded-md">
            <section id="group{i+1}-section1">
              {decoded_html}
            </section>

            <section id="group{i+1}-section2" class="hidden">
            <pre
          class="flex overflow-auto bg-black rounded-b-lg text-sm leading-[1.5714285714] text-white sm:rounded-t-lg language-html">
        
              {code_tag}
              </pre>
            </section>
            </div>
          </div>
          """
        final_html = final_html + new_extracted_html

    final_html = (
        final_html
        + f""" </body>
          <script>
              function toggleSections(group) {{
              var section1 = document.getElementById(`${{group}}-section1`);
              var section2 = document.getElementById(`${{group}}-section2`);

              if (section1.style.display === 'none') {{
                section1.style.display = 'block';
                section2.style.display = 'none';
              }} else {{
              section1.style.display = 'none';
              section2.style.display = 'block';
              }}
            }}
          </script>
        </html>"""
    )

    with open(links_file, "w") as links_output_file:
        links_output_file.write(final_html)

    print(f"Extracted {len(code_tags)} HTML code blocks")
    print(f"Links to the created HTML files saved in '{links_file}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract HTML code from <code> tags and save to separate files."
    )
    parser.add_argument("input_html", help="Input HTML file to process")
    parser.add_argument(
        "links_file", help="Output file to save links to created HTML files"
    )
    args = parser.parse_args()

    extract_code_tags(args.input_html, args.links_file)
