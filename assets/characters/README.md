# Character sheets (local copies)

Local copies of the Higgsfield character sheets, so any machine can run the QC face check and re-upload a reference when the registry's IDs aren't reachable from its Higgsfield workspace (SETUP.md, "Adding a teammate"). The registry (registry/assets.json) stays the source of truth for IDs; regenerate these copies when a sheet changes.

| File | Character | Registry sheet ID | Used by |
|---|---|---|---|
| pandey_sheet_v2.jpg | pandey | `0e19cfb4-46bc-431c-9e8f-5015416124c7` | QC identity reference: shot_spec.py SHEETS, qc_gate face check, face_consistency.py |
| billu_sheet.jpg | billu | `077c7b16-5911-4a12-838c-1adde9fc0ea9` | keyframe reference (Sahayata Kendra) |
| sarika_sheet.jpg | sarika | `85391de0-1855-486d-9e6b-0e7c841fc038` | keyframe reference (Samachar) |
| gupta_sheet.jpg | gupta | `b51d1f5e-bad5-4f00-af03-f55ff28ed8a0` | keyframe reference (Samachar) |
| rahul_sheet.jpg | rahul | `8bfe4cbc-c483-455a-a9fc-c1080f1fb435` | keyframe reference (Teleshop) |
| sachdev_sheet.jpg | sachdev | `0e4faf46-aa1e-4c29-b2b9-dd2d84f5b2e2` | keyframe reference (Teleshop) |

JPEG at quality 92: face_consistency scored E7's front keyframe 0.77 against this copy and 0.73 against the original PNG (same character >= 0.55; different characters 0.10-0.34).
