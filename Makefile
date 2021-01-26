%.dxf: %.scad
	openscad $< -o $@

%.scad: %.py cad.py layout.py
	python $< > $@

.PHONY: clean
clean:
	rm -rf *.scad *.dxf left/ right/ left.zip right.zip

.PHONY: case_panels
case_panels: lower_panel.dxf upper_panel.dxf

.PHONY: pcb_layout
pcb_layout: pcb_outline.dxf
	python pcb_layout.py ./hardware/aya.kicad_pcb

left/left.kicad_pcb: hardware/aya.kicad_pcb
	mkdir -p "$(shell dirname $@)"
	kikit panelize extractboard -s -220 -25 200 140 $< $@

right/right.kicad_pcb: hardware/aya.kicad_pcb
	mkdir -p "$(shell dirname $@)"
	kikit panelize extractboard -s   20 -25 200 140 $< $@

.PHONY: pcb_split
pcb_split: left/left.kicad_pcb right/right.kicad_pcb

left.zip: left/left.kicad_pcb
	zip $@ left/*.gbr left/*.drl

right.zip: right/right.kicad_pcb
	zip $@ right/*.gbr right/*.drl

.PHONY: pcb_gerbers
pcb_gerbers: left.zip right.zip
