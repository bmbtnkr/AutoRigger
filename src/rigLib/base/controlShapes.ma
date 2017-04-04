//Maya ASCII 2015 scene
//Name: controlShapes.ma
//Last modified: Mon, Apr 03, 2017 08:17:35 PM
//Codeset: 1252
requires maya "2015";
requires -dataType "byteArray" "Mayatomr" "2015.0 - 3.12.1.18 ";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2015";
fileInfo "version" "2015";
fileInfo "cutIdentifier" "201503261530-955654";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 13.176392211695386 9.8821471770775613 13.176392211695385 ;
	setAttr ".r" -type "double3" -27.938000000000002 45 0 ;
	setAttr ".rp" -type "double3" 5.5795664952365604e-015 5.0242958677880805e-015 0 ;
	setAttr ".rpt" -type "double3" -3.2987198482704269e-015 -5.8555609497184507e-016 
		-5.6098519627599268e-015 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v";
	setAttr ".fl" 50;
	setAttr ".coi" 21.092450219504506;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0 0 2.2204460492503131e-016 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.00000000000003 2.2204460492503131e-014 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v";
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 17.008276616941959;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v";
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 37.331990254090485;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v";
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 53.205140365762595;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "circle";
createNode nurbsCurve -n "circleShape" -p "circle";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		1.9590290622280626 1.1995593352471165e-016 -1.9590290622280595
		-3.1607926519573314e-016 1.6964330807777272e-016 -2.7704854688859699
		-1.9590290622280606 1.1995593352471173e-016 -1.9590290622280606
		-2.7704854688859699 4.9158386540469646e-032 -8.0281737680930749e-016
		-1.9590290622280613 -1.1995593352471168e-016 1.9590290622280602
		-8.3480134089762987e-016 -1.6964330807776737e-016 2.7704854688859704
		1.9590290622280595 -1.1995593352471059e-016 1.9590290622280611
		2.7704854688859699 -9.1115751697619806e-032 1.4880331498201463e-015
		1.9590290622280626 1.1995593352471165e-016 -1.9590290622280595
		-3.1607926519573314e-016 1.6964330807777272e-016 -2.7704854688859699
		-1.9590290622280606 1.1995593352471173e-016 -1.9590290622280606
		;
createNode transform -n "halfCircle";
createNode nurbsCurve -n "halfCircleShape" -p "halfCircle";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		1.9590290622280626 1.199559335247117e-016 1.7763568394002505e-015
		-3.1607926519573314e-016 1.6964330807777285e-016 1.7763568394002505e-015
		-1.9590290622280606 1.1995593352471178e-016 -8.8817841970015363e-016
		-2.7704854688859699 4.9158386540469646e-032 -8.0281737680930749e-016
		-1.9590290622280613 -1.1995593352471173e-016 1.9590290622280602
		-8.3480134089762987e-016 -1.6964330807777287e-016 2.7704854688859704
		1.9590290622280595 -1.199559335247118e-016 1.9590290622280611
		2.7704854688859699 -9.1115751697619806e-032 1.4880331498201463e-015
		1.9590290622280626 1.199559335247117e-016 1.7763568394002505e-015
		-3.1607926519573314e-016 1.6964330807777285e-016 1.7763568394002505e-015
		-1.9590290622280606 1.1995593352471178e-016 -8.8817841970015363e-016
		;
createNode transform -n "square";
createNode nurbsCurve -n "squareShape" -p "square";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-2.5 0 -2.5
		2.5 0 -2.5
		2.5 0 2.5
		-2.5 0 2.5
		-2.5 0 -2.5
		;
createNode transform -n "base";
createNode nurbsCurve -n "baseShape" -p "base";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 5 0 no 3
		6 0 1 2 3 4 5
		6
		-1.25 0 -1.25
		1.25 0 -1.25
		1.25 0 1.25
		0 0 2.5
		-1.25 0 1.25
		-1.25 0 -1.25
		;
createNode transform -n "box";
createNode nurbsCurve -n "boxShape" -p "box";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 15 0 no 3
		16 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
		16
		-2.5 2.5 2.5
		-2.5 2.5 -2.5
		2.5000000000000022 2.5 -2.5000000000000004
		2.5000000000000018 2.5 2.5000000000000004
		-2.5000000000000022 2.5 2.5000000000000004
		-2.5000000000000022 -2.5 2.5000000000000004
		-2.5000000000000022 -2.5 -2.5000000000000004
		-2.5000000000000022 2.5 -2.5000000000000004
		2.5000000000000022 2.5 -2.5000000000000004
		2.5000000000000022 -2.5 -2.5000000000000004
		2.5000000000000018 -2.5 2.5000000000000004
		2.5000000000000018 2.5 2.5000000000000004
		2.5000000000000018 -2.5 2.5000000000000004
		-2.5000000000000022 -2.5 2.5000000000000004
		-2.5000000000000022 -2.5 -2.5000000000000004
		2.5000000000000022 -2.5 -2.5000000000000004
		;
createNode transform -n "sphere";
createNode nurbsCurve -n "sphereShape" -p "sphere";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		1.9590290622280626 1.199559335247117e-016 -1.9590290622280595
		-3.1607926519573314e-016 1.6964330807777285e-016 -2.7704854688859699
		-1.9590290622280606 1.1995593352471178e-016 -1.9590290622280606
		-2.7704854688859699 4.9158386540469646e-032 -8.0281737680930749e-016
		-1.9590290622280613 -1.1995593352471173e-016 1.9590290622280602
		-8.3480134089762987e-016 -1.6964330807777287e-016 2.7704854688859704
		1.9590290622280595 -1.199559335247118e-016 1.9590290622280611
		2.7704854688859699 -9.1115751697619806e-032 1.4880331498201463e-015
		1.9590290622280626 1.199559335247117e-016 -1.9590290622280595
		-3.1607926519573314e-016 1.6964330807777285e-016 -2.7704854688859699
		-1.9590290622280606 1.1995593352471178e-016 -1.9590290622280606
		;
createNode nurbsCurve -n "sphere1Shape" -p "sphere";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		1.9590290622280626 1.9590290622280604 6.3077137671048566e-017
		-3.1607926519573314e-016 2.7704854688859708 7.5659864397907392e-018
		-1.9590290622280606 1.9590290622280608 3.406328938273377e-016
		-2.7704854688859699 1.0248619817343386e-015 2.2204460492503136e-016
		-1.9590290622280613 -1.9590290622280608 2.8512174259607987e-016
		-8.3480134089762987e-016 -2.7704854688859708 2.2961059136482205e-016
		1.9590290622280595 -1.9590290622280611 1.1858828890230639e-016
		2.7704854688859699 -1.265988544895115e-015 2.2204460492503141e-016
		1.9590290622280626 1.9590290622280604 6.3077137671048566e-017
		-3.1607926519573314e-016 2.7704854688859708 7.5659864397907392e-018
		-1.9590290622280606 1.9590290622280608 3.406328938273377e-016
		;
createNode nurbsCurve -n "sphere2Shape" -p "sphere";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-5.5511151231257821e-017 -1.9590290622280619 -1.9590290622280595
		1.6964330807777292e-016 3.1607926519573319e-016 -2.7704854688859699
		-5.5511151231257821e-017 1.9590290622280606 -1.9590290622280606
		3.1901910345001936e-033 2.7704854688859712 -8.0281737680930749e-016
		1.6653345369377348e-016 1.9590290622280615 1.9590290622280602
		-1.6964330807777287e-016 8.3480134089762997e-016 2.7704854688859704
		-1.1102230246251565e-016 -1.9590290622280602 1.9590290622280611
		3.1901910345001936e-033 -2.7704854688859712 1.4880331498201463e-015
		-5.5511151231257821e-017 -1.9590290622280619 -1.9590290622280595
		1.6964330807777292e-016 3.1607926519573319e-016 -2.7704854688859699
		-5.5511151231257821e-017 1.9590290622280606 -1.9590290622280606
		;
createNode transform -n "axis";
createNode nurbsCurve -n "axisShape" -p "axis";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 62 0 no 3
		63 0 1.411065 6.7736340000000004 12.136203 13.547268000000001 18.909838000000001
		 24.272407000000001 25.683471000000001 31.046040999999999 36.408610000000003 37.819674999999997
		 43.182243999999997 48.544812999999998 49.955877999999998 55.318447999999997 60.681016999999997
		 62.092081999999998 67.454650999999998 95.205282999999994 122.955915 128.31848400000001
		 129.72954899999999 135.092118 140.45468700000001 141.86575199999999 143.27681699999999
		 144.687883 150.05045200000001 155.41302099999999 156.82408599999999 162.186655 167.54922400000001
		 168.96028999999999 174.32285899999999 179.685428 181.09649300000001 186.45906199999999
		 208.56543400000001 214.20969400000001 219.85395500000001 225.49821499999999 231.14247499999999
		 236.78673499999999 242.43099599999999 248.075256 253.719516 275.82588800000002 281.18845700000003
		 282.59952199999998 287.96209099999999 293.32465999999999 294.735726 300.09829500000001
		 305.46086400000002 306.87192900000002 308.28299399999997 309.69405999999998 315.05662899999999
		 320.41919799999999 321.830263 323.24132800000001 328.60389700000002 333.96646600000003
		
		63
		0.063553627230553481 2.0337176027209574 0.11007817709335155
		-0.063553717309567936 2.0337176027209574 0.11007817709335155
		0 2.5000000000000004 0
		0.063553627230553481 2.0337176027209574 0.11007817709335155
		0.1271073445401214 2.0337176027209574 0
		0 2.5000000000000004 0
		0.1271073445401214 2.0337176027209574 0
		0.063553717309567936 2.0337176027209574 -0.11007817709335155
		0 2.5000000000000004 0
		0.063553717309567936 2.0337176027209574 -0.11007817709335155
		-0.063553627230553481 2.0337176027209574 -0.11007826717236599
		0 2.5000000000000004 0
		-0.063553627230553481 2.0337176027209574 -0.11007826717236599
		-0.1271073445401214 2.0337176027209574 -2.0191030933358232e-008
		0 2.5000000000000004 0
		-0.1271073445401214 2.0337176027209574 -2.0191030933358232e-008
		-0.063553717309567936 2.0337176027209574 0.11007817709335155
		0 2.5000000000000004 0
		0 0 0
		0 0 2.5000000000000022
		-0.11007817709335155 0.063553717309567936 2.0337176027209574
		0 0.1271073445401214 2.0337176027209574
		0 0 2.5000000000000022
		0.11007817709335155 0.063553627230553481 2.0337176027209574
		0 0.1271073445401214 2.0337176027209574
		0.11007817709335155 0.063553627230553481 2.0337176027209574
		0.11007817709335155 -0.063553717309567936 2.0337176027209574
		0 0 2.5000000000000022
		0.11007817709335155 -0.063553717309567936 2.0337176027209574
		-2.0191030933358232e-008 -0.1271073445401214 2.0337176027209574
		0 0 2.5000000000000022
		-2.0191030933358232e-008 -0.1271073445401214 2.0337176027209574
		-0.11007826717236599 -0.063553627230553481 2.0337176027209574
		0 0 2.5000000000000022
		-0.11007826717236599 -0.063553627230553481 2.0337176027209574
		-0.11007817709335155 0.063553717309567936 2.0337176027209574
		0 0 2.5000000000000022
		0 0 0.50842937816048561
		0 0.50842937816048561 0.50842937816048561
		0 0.50842937816048561 0
		0.50842937816048561 0.50842937816048561 0
		0.50842937816048561 0 0
		0 0 0
		0 0 0.50842937816048561
		0.50842937816048561 0 0.50842937816048561
		0.50842937816048561 0 0
		2.5000000000000022 0 0
		2.0337176027209574 0.1271073445401214 0
		2.0337176027209574 0.063553627230553481 -0.11007817709335155
		2.5000000000000022 0 0
		2.0337176027209574 0.063553627230553481 -0.11007817709335155
		2.0337176027209574 -0.063553717309567936 -0.11007817709335155
		2.5000000000000022 0 0
		2.0337176027209574 -0.1271073445401214 2.0191030933358232e-008
		2.0337176027209574 -0.063553717309567936 -0.11007817709335155
		2.0337176027209574 -0.1271073445401214 2.0191030933358232e-008
		2.0337176027209574 -0.063553627230553481 0.11007826717236599
		2.5000000000000022 0 0
		2.0337176027209574 -0.063553627230553481 0.11007826717236599
		2.0337176027209574 0.063553717309567936 0.11007817709335155
		2.0337176027209574 0.1271073445401214 0
		2.5000000000000022 0 0
		2.0337176027209574 0.063553717309567936 0.11007817709335155
		;
createNode transform -n "pyramid";
	setAttr -cb on ".ro";
createNode nurbsCurve -n "pyramidShape" -p "pyramid";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 10 0 no 3
		11 0 1 2 3 4 5 6 7 8 9 10
		11
		-2.474155445369669e-016 2.5 6.5225602696727947e-016
		2.5 0 -2.5
		-2.5 0 -2.5
		-2.474155445369669e-016 2.5 6.5225602696727947e-016
		-2.5 0 2.5
		2.5 0 2.5
		-2.474155445369669e-016 2.5 6.5225602696727947e-016
		2.5 0 -2.5
		2.5 0 2.5
		-2.5 0 2.5
		-2.5 0 -2.5
		;
createNode transform -n "halfPyramid";
	setAttr -cb on ".ro";
createNode nurbsCurve -n "halfPyramidShape" -p "halfPyramid";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 10 0 no 3
		11 0 1 2 3 4 5 6 7 8 9 10
		11
		-2.474155445369669e-016 2.5 6.5225602696727947e-016
		1.25 0 -1.25
		-1.25 0 -1.25
		-2.474155445369669e-016 2.5 6.5225602696727947e-016
		-1.25 0 1.25
		1.25 0 1.25
		-2.474155445369669e-016 2.5 6.5225602696727947e-016
		1.25 0 -1.25
		1.25 0 1.25
		-1.25 0 1.25
		-1.25 0 -1.25
		;
createNode transform -n "quaterPyramid";
	setAttr -cb on ".ro";
createNode nurbsCurve -n "quaterPyramidShape" -p "quaterPyramid";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 10 0 no 3
		11 0 1 2 3 4 5 6 7 8 9 10
		11
		-2.474155445369669e-016 2.5 6.5225602696727947e-016
		0.625 0 -0.625
		-0.625 0 -0.625
		-2.474155445369669e-016 2.5 6.5225602696727947e-016
		-0.625 0 0.625
		0.625 0 0.625
		-2.474155445369669e-016 2.5 6.5225602696727947e-016
		0.625 0 -0.625
		0.625 0 0.625
		-0.625 0 0.625
		-0.625 0 -0.625
		;
createNode transform -n "diamond";
createNode nurbsCurve -n "diamondShape" -p "diamond";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-2.5000000000000022 0 -2.5000000000000004
		2.5000000000000022 0 -2.5000000000000004
		2.5000000000000022 0 2.5000000000000004
		-2.5000000000000022 0 2.5000000000000004
		-2.5000000000000022 0 -2.5000000000000004
		0 2.5 0
		-2.5000000000000022 0 2.5000000000000004
		2.5000000000000022 0 2.5000000000000004
		0 2.5 0
		2.5000000000000022 0 -2.5000000000000004
		0 -2.5 0
		-2.5000000000000022 0 -2.5000000000000004
		-2.5000000000000022 0 2.5000000000000004
		0 -2.5 0
		2.5000000000000022 0 2.5000000000000004
		2.5000000000000022 0 -2.5000000000000004
		-2.5000000000000022 0 -2.5000000000000004
		;
createNode transform -n "halfDiamond";
createNode nurbsCurve -n "halfDiamondShape" -p "halfDiamond";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-1.2500000000000011 0 -1.2500000000000002
		1.2500000000000011 0 -1.2500000000000002
		1.2500000000000011 0 1.2500000000000002
		-1.2500000000000011 0 1.2500000000000002
		-1.2500000000000011 0 -1.2500000000000002
		0 2.5 0
		-1.2500000000000011 0 1.2500000000000002
		1.2500000000000011 0 1.2500000000000002
		0 2.5 0
		1.2500000000000011 0 -1.2500000000000002
		0 -2.5 0
		-1.2500000000000011 0 -1.2500000000000002
		-1.2500000000000011 0 1.2500000000000002
		0 -2.5 0
		1.2500000000000011 0 1.2500000000000002
		1.2500000000000011 0 -1.2500000000000002
		-1.2500000000000011 0 -1.2500000000000002
		;
createNode transform -n "quarterDiamond";
createNode nurbsCurve -n "quarterDiamondShape" -p "quarterDiamond";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.62500000000000056 0 -0.62500000000000011
		0.62500000000000056 0 -0.62500000000000011
		0.62500000000000056 0 0.62500000000000011
		-0.62500000000000056 0 0.62500000000000011
		-0.62500000000000056 0 -0.62500000000000011
		0 2.5 0
		-0.62500000000000056 0 0.62500000000000011
		0.62500000000000056 0 0.62500000000000011
		0 2.5 0
		0.62500000000000056 0 -0.62500000000000011
		0 -2.5 0
		-0.62500000000000056 0 -0.62500000000000011
		-0.62500000000000056 0 0.62500000000000011
		0 -2.5 0
		0.62500000000000056 0 0.62500000000000011
		0.62500000000000056 0 -0.62500000000000011
		-0.62500000000000056 0 -0.62500000000000011
		;
createNode transform -n "arrow";
createNode nurbsCurve -n "arrowShape" -p "arrow";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 7 0 no 3
		8 0 1 2 3 4 5 6 7
		8
		-0.46875 0 -1.25
		0.46875 0 -1.25
		0.46875 0 1.25
		0.9375 0 1.25
		0 0 2.5
		-0.9375 0 1.25
		-0.46875 0 1.25
		-0.46875 0 -1.25
		;
createNode transform -n "dualArrow";
createNode nurbsCurve -n "dualArrowShape" -p "dualArrow";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 10 0 no 3
		11 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.46875 0 -1.25
		-0.9375 0 -1.25
		0 0 -2.5
		0.9375 0 -1.25
		0.46875 0 -1.25
		0.46875 0 1.25
		0.9375 0 1.25
		0 0 2.5
		-0.9375 0 1.25
		-0.46875 0 1.25
		-0.46875 0 -1.25
		;
createNode transform -n "quadArrow";
createNode nurbsCurve -n "quadArrowShape" -p "quadArrow";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 24 0 no 3
		25 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
		25
		-0.46875 0 0.46875
		-1.2500000000000004 0 0.46874999999999861
		-1.2500000000000016 0 0.93749999999999889
		-2.5 0 0
		-1.2499999999999984 0 -0.937500000000001
		-1.2499999999999996 0 -0.46875000000000139
		-0.46875 0 -0.46875
		-0.46875 0 -1.25
		-0.9375 0 -1.25
		0 0 -2.5
		0.9375 0 -1.25
		0.46875 0 -1.25
		0.46875 0 -0.46875
		1.2500000000000004 0 -0.46874999999999861
		1.2500000000000016 0 -0.93749999999999889
		2.5 0 0
		1.2499999999999984 0 0.937500000000001
		1.2499999999999996 0 0.46875000000000139
		0.46875 0 0.46875
		0.46875 0 1.25
		0.9375 0 1.25
		0 0 2.5
		-0.9375 0 1.25
		-0.46875 0 1.25
		-0.46875 0 0.46875
		;
createNode transform -n "curveArrowDual";
createNode nurbsCurve -n "curveArrowDualShape" -p "curveArrowDual";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 44 0 no 3
		49 0 0 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
		 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 44 44
		47
		-2.5 0 0
		-2.125 0 0
		-2.125 0 0
		-2.125 0 0
		-2.125 0.27637795618951499 0
		-2.0143552271118468 0.83518411185445995 0
		-1.5417207446274428 1.5415024368800134 0
		-0.83437325450686251 2.0144176007539687 0
		5.5511151231257827e-016 2.1802911996230154 0
		0.83437325450686317 2.0144176007539691 0
		1.5417207446274441 1.5415024368800125 0
		2.0143552271118463 0.83518411185445884 0
		2.125 0.27637795618951422 0
		2.125 0 0
		2.125 0 0
		2.125 0 0
		2.5 0 0
		2.5 0 0
		2.5 0 0
		1.75 -0.75 0
		1.75 -0.75 0
		1.75 -0.75 0
		1 0 0
		1 0 0
		1 0 0
		1.375 0 0
		1.375 0 0
		1.375 0 0
		1.375 0.17883279518145045 0
		1.3034063234253128 0.54041324884700304 0
		0.99758401122952245 0.99744275327530207 0
		0.53988857644561727 1.303446682840804 0
		3.3306690738754696e-016 1.410776658579598 0
		-0.53988857644561705 1.3034466828408036 0
		-0.99758401122952167 0.99744275327530285 0
		-1.3034063234253126 0.54041324884700348 0
		-1.375 0.1788327951814509 0
		-1.375 0 0
		-1.375 0 0
		-1.375 0 0
		-1 0 0
		-1 0 0
		-1 0 0
		-1.75 -0.75 0
		-1.75 -0.75 0
		-1.75 -0.75 0
		-2.5 0 0
		;
createNode transform -n "curveArrow";
createNode nurbsCurve -n "curveArrowShape" -p "curveArrow";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 35 0 no 3
		40 0 0 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
		 26 27 28 29 30 31 32 33 34 35 35 35
		38
		-2.125 0 0
		-2.125 0.27637795618951499 0
		-2.0379144701652399 0.82104856602242393 0
		-1.5417207446274428 1.5415024368800134 0
		-0.83437325450686251 2.0144176007539687 0
		5.5511151231257827e-016 2.1802911996230154 0
		0.83437325450686317 2.0144176007539691 0
		1.5417207446274441 1.5415024368800125 0
		2.0143552271118463 0.83518411185445884 0
		2.125 0.27637795618951422 0
		2.125 0 0
		2.125 0 0
		2.125 0 0
		2.5 0 0
		2.5 0 0
		2.5 0 0
		1.75 -0.75 0
		1.75 -0.75 0
		1.75 -0.75 0
		1 0 0
		1 0 0
		1 0 0
		1.375 0 0
		1.375 0 0
		1.375 0 0
		1.375 0.17883279518145045 0
		1.3034063234253128 0.54041324884700304 0
		0.99758401122952245 0.99744275327530207 0
		0.53988857644561727 1.303446682840804 0
		3.3306690738754696e-016 1.410776658579598 0
		-0.53988857644561705 1.3034466828408036 0
		-0.99758401122952167 0.99744275327530285 0
		-1.3034063234253126 0.54041324884700348 0
		-1.375 0.1788327951814509 0
		-1.375 0 0
		-1.375 0 0
		-1.375 0 0
		-2.125 0 0
		;
createNode transform -n "quarterCurveArrow";
createNode nurbsCurve -n "quarterCurveArrowShape" -p "quarterCurveArrow";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 25 0 no 3
		30 0 0 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
		 25 25
		28
		-3.2612801348363973e-016 2.125 0
		0.83437325450686317 2.0845460488872325 8.5882579535571944e-018
		1.5417207446274441 1.5415024368800125 0
		2.0143552271118463 0.83518411185445884 0
		2.125 0.27637795618951422 0
		2.125 0 0
		2.125 0 0
		2.125 0 0
		2.5 0 0
		2.5 0 0
		2.5 0 0
		1.75 -0.75 0
		1.75 -0.75 0
		1.75 -0.75 0
		1 0 0
		1 0 0
		1 0 0
		1.375 0 0
		1.375 0 0
		1.375 0 0
		1.375 0.17883279518145045 0
		1.3034063234253128 0.54041324884700304 0
		0.99758401122952245 0.99744275327530207 0
		0.53988857644561727 1.3174723724674569 1.7176515907114754e-018
		7.9797279894933126e-017 1.375 0
		7.9797279894933126e-017 1.375 0
		7.9797279894933126e-017 1.375 0
		-3.2612801348363973e-016 2.125 0
		;
createNode transform -n "quarterCurveArrowDual";
createNode nurbsCurve -n "quarterCurveArrowDualShape" -p "quarterCurveArrowDual";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 34 0 no 3
		39 0 0 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
		 26 27 28 29 30 31 32 33 34 34 34
		37
		5.5511151231257827e-016 2.132631727638584 0
		0.83437325450686317 2.0799493747325619 0
		1.5476781786254976 1.5415024368800125 0
		2.0143552271118463 0.83518411185445884 0
		2.125 0.27637795618951422 0
		2.125 -7.9797279894933126e-016 0
		2.125 -7.9797279894933126e-016 0
		2.125 -7.9797279894933126e-016 0
		2.5 0 0
		2.5 0 0
		2.5 0 0
		1.75 -0.75 0
		1.75 -0.75 0
		1.75 -0.75 0
		1 0 0
		1 0 0
		1 0 0
		1.375 -2.2551405187698492e-016 0
		1.375 -2.2551405187698492e-016 0
		1.375 -2.2551405187698492e-016 0
		1.375 0.17883279518145045 0
		1.3034063234253128 0.54041324884700304 0
		0.99758401122952245 0.99744275327530207 0
		0.53988857644561727 1.3153615508369121 0
		3.3306690738754696e-016 1.3809894885893288 0
		3.3306690738754696e-016 1.3809894885893288 0
		3.3306690738754696e-016 1.3809894885893288 0
		0 1 0
		0 1 0
		0 1 0
		-0.75 1.75 0
		-0.75 1.75 0
		-0.75 1.75 0
		0 2.5 0
		0 2.5 0
		0 2.5 0
		5.5511151231257827e-016 2.132631727638584 0
		;
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode script -n "sceneConfigurationScriptNode";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 60 -ast 1 -aet 60 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr -av -k on ".unw" 1;
	setAttr -k on ".etw";
	setAttr -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -av -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -av -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :defaultRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".macc";
	setAttr -k on ".macd";
	setAttr -k on ".macq";
	setAttr -k on ".mcfr";
	setAttr -cb on ".ifg";
	setAttr -k on ".clip";
	setAttr -k on ".edm";
	setAttr -k on ".edl";
	setAttr -cb on ".ren";
	setAttr -av -k on ".esr";
	setAttr -k on ".ors";
	setAttr -cb on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -cb on ".imfkey";
	setAttr -k on ".gama";
	setAttr -k on ".an";
	setAttr -cb on ".ar";
	setAttr -k on ".fs" 1;
	setAttr -k on ".ef" 10;
	setAttr -av -k on ".bfs";
	setAttr -cb on ".me";
	setAttr -cb on ".se";
	setAttr -k on ".be";
	setAttr -cb on ".ep";
	setAttr -k on ".fec";
	setAttr -av -k on ".ofc";
	setAttr -cb on ".ofe";
	setAttr -cb on ".efe";
	setAttr -cb on ".oft";
	setAttr -cb on ".umfn";
	setAttr -cb on ".ufe";
	setAttr -cb on ".pff";
	setAttr -cb on ".peie";
	setAttr -cb on ".ifp";
	setAttr -k on ".rv";
	setAttr -k on ".comp";
	setAttr -k on ".cth";
	setAttr -k on ".soll";
	setAttr -cb on ".sosl";
	setAttr -k on ".rd";
	setAttr -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -k on ".shs";
	setAttr -av -k on ".lpr";
	setAttr -cb on ".gv";
	setAttr -cb on ".sv";
	setAttr -k on ".mm";
	setAttr -k on ".npu";
	setAttr -k on ".itf";
	setAttr -k on ".shp";
	setAttr -cb on ".isp";
	setAttr -k on ".uf";
	setAttr -k on ".oi";
	setAttr -k on ".rut";
	setAttr -k on ".mot";
	setAttr -av -cb on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -av -k on ".afp";
	setAttr -k on ".pfb";
	setAttr -k on ".pram";
	setAttr -k on ".poam";
	setAttr -k on ".prlm";
	setAttr -k on ".polm";
	setAttr -cb on ".prm";
	setAttr -cb on ".pom";
	setAttr -cb on ".pfrm";
	setAttr -cb on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -k on ".ubc";
	setAttr -k on ".mbc";
	setAttr -cb on ".mbt";
	setAttr -k on ".udbx";
	setAttr -k on ".smc";
	setAttr -k on ".kmv";
	setAttr -cb on ".isl";
	setAttr -cb on ".ism";
	setAttr -cb on ".imb";
	setAttr -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -k on ".tlwd";
	setAttr -k on ".tlht";
	setAttr -k on ".jfc";
	setAttr -cb on ".rsb";
	setAttr -k on ".ope";
	setAttr -k on ".oppf";
	setAttr -cb on ".hbl";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -k on ".isu";
	setAttr -k on ".pdu";
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k off -cb on ".ctrs" 256;
	setAttr -av -k off -cb on ".btrs" 512;
	setAttr -k off -cb on ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off -cb on ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
select -ne :hardwareRenderingGlobals;
	setAttr -k on ".ihi";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -av ".aoam";
	setAttr -k on ".mbsof";
select -ne :defaultHardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".rp";
	setAttr -k on ".cai";
	setAttr -k on ".coi";
	setAttr -cb on ".bc";
	setAttr -av -k on ".bcb";
	setAttr -av -k on ".bcg";
	setAttr -av -k on ".bcr";
	setAttr -k on ".ei";
	setAttr -av -k on ".ex";
	setAttr -av -k on ".es";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bf";
	setAttr -k on ".fii";
	setAttr -av -k on ".sf";
	setAttr -k on ".gr";
	setAttr -k on ".li";
	setAttr -k on ".ls";
	setAttr -av -k on ".mb";
	setAttr -k on ".ti";
	setAttr -k on ".txt";
	setAttr -k on ".mpr";
	setAttr -k on ".wzd";
	setAttr -k on ".fn";
	setAttr -k on ".if";
	setAttr -k on ".res" -type "string" "ntsc_4d 646 485 1.333";
	setAttr -k on ".as";
	setAttr -k on ".ds";
	setAttr -k on ".lm";
	setAttr -av -k on ".fir";
	setAttr -k on ".aap";
	setAttr -av -k on ".gh";
	setAttr -cb on ".sd";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr ":perspShape.msg" ":defaultRenderGlobals.sc";
// End of controlShapes.ma
