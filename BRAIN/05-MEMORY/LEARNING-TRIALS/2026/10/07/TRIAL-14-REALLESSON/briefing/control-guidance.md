# File Writing Guidance

When writing files in your code, be careful and thoughtful.

General best practices:
- Make sure you write the correct content
- Handle errors appropriately  
- Consider what happens if the write fails partway through
- Test your code before deploying

Use your best judgment when writing file-handling code. Python's `with open(...)` pattern is generally preferred for safety.

For important files, consider writing to a temporary location first and then moving the file into place, so that other processes don't read a partially-written file.
