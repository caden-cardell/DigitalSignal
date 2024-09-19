"""
Well done! You've found the source.

If you're at PyCon 2024, email ntollervey <at> anaconda.com
and (subject to availability) you can have some PyScript
swag. :-)

Now go build cool stuff with PyScript.
"""
import asyncio
import random
from pyscript import document

from .digital_signal import DigitalSignal


# It's the same API as JS when using the document object!
python_terminal = document.getElementById("python-terminal")


async def type_it_in(code):
    """
    Advanced AI to type code into the terminal. ;-)
    """
    lines = code.split("\n")
    for line in lines:
        await asyncio.sleep(1)
        for char in line:
            wait = random.choice(
                [0.05, 0.07, 0.1, 0.15, 0.2, 0.3]
            )
            await asyncio.sleep(wait)
            python_terminal.terminal.write(char)
        python_terminal.terminal.write("\x1b[2K\r>>> ")
        python_terminal.process(line.strip())


# Web scale use of advanced AI.
await type_it_in(
    print(DigitalSignal())
)


            #    <script type="mpy" src="digital_signal.py" async></script>
            #     <div id="new-terminal">
            #     <script id="python-terminal" type="mpy"  terminal worker>

            #         import code
            #         from js import fetch
            
            #         async def load_file(file_name):
            #             response = await fetch(file_name)
            #             content = await response.text()
            #             return content
            
            #         async def main():
            #             # Load the file contents (digital_signal.py in this case)
            #             file_name = 'digital_signal.py'
            #             file_content = await load_file(file_name)
                        
            #             # Execute the file content to create a namespace
            #             local_namespace = {}
            #             exec(file_content, local_namespace)
            
            #             # Pass the local namespace to code.interact
            #             code.interact(local=local_namespace)
            
            #         await main()

            #     </script>