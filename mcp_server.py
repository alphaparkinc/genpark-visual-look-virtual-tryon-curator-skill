# -*- coding: utf-8 -*-
"""
Glance Visual Look & Virtual Try-On Curator MCP Server
Exposes look curation tools via standard JSON-RPC 2.0 over STDIO.
"""

import sys
import json
from client import GlanceVisualLookVirtualTryOnCurator

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "glance-visual-look-virtual-tryon-curator", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "curate_outfit_lookbook",
                        "description": "Synthesizes context-aware fashion outfits and personalized editorial lookbooks matching user aesthetics, weather, and occasion.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "user_aesthetic_vector": {"type": "object", "description": "Key-value map of user style preferences (e.g. Quiet Luxury, Minimalist)"},
                                "ambient_temperature_c": {"type": "number", "description": "Ambient outdoor temperature in Celsius"},
                                "target_occasion": {"type": "string", "description": "Occasion code (CASUAL_WEEKEND, SMART_CASUAL, BUSINESS_FORMAL, EVENING_GALA)"}
                            },
                            "required": ["user_aesthetic_vector"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "curate_outfit_lookbook":
            curator = GlanceVisualLookVirtualTryOnCurator()
            res = curator.curate_outfit_lookbook(
                user_aesthetic_vector=args.get("user_aesthetic_vector", {"Quiet Luxury": 0.8, "Minimalist": 0.7}),
                ambient_temperature_c=args.get("ambient_temperature_c", 20.0),
                target_occasion=args.get("target_occasion", "SMART_CASUAL"),
                candidate_items=args.get("candidate_items")
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": f"Method '{method}' not supported"}}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MCP Server Discovery Test OK")
        curator = GlanceVisualLookVirtualTryOnCurator()
        test_res = curator.curate_outfit_lookbook({"Quiet Luxury": 0.9, "Minimalist": 0.8}, 16.0, "BUSINESS_FORMAL")
        print(f"Test Curated Score: {test_res['overall_compatibility_pct']}%")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
