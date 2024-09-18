# Musescore pipeline #101

💡 Vychází z [pipeline 100](pipeline_100.md) a je stejná až po **6_copied_pairs** včetně.

💡 DŮLEŽITÝ NASTAVENÍ Musescore → Edit → Preferences → Import → Import layout + page breaks

- **7_yolo_detected**: resize staves back to pages (1024x1458, for YOLO detector to work better, overwrite), detect staves by YOLO, copy only labels that have detected stave in output dir
