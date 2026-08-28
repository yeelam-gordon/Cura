# Change Design

This is a coordinated two-repository change:

1. `Ultimaker/cura-workflows`: correct the Arm CRT path, restore workflow robustness, and add package validation.
2. `Ultimaker/Cura`: point the test fork at the modified reusable workflow and update the Arm dispatcher as required.

Detailed package and workflow designs:

- [02-cura-package-audit.md](02-cura-package-audit.md)
- [03-cura-workflows-audit.md](03-cura-workflows-audit.md)
