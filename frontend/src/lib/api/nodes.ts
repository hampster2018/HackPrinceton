import { writable, get } from "svelte/store";
import type { Writable } from "svelte/store";
import { selectedTextbook } from "./textbooks";
import { localURL } from "./config";

export interface Node {
  id: number;
  label: string;
  color: string;
  group: string;
  completed?: boolean;
}

interface Edge {
  from: number;
  to: number;
}

export const refresh: Writable<boolean> = writable(false);
export const nodes : Writable<Node[]> = writable();
export const edges : Writable<Edge[]> = writable();
export const selectedNode : Writable<number | null> = writable(null);
export const nodeNames : Writable<string[]> = writable([]);

export const completeNode = async (selectedNode : number) => {

  fetch(localURL + `/update_completion?textbook_name=${get(selectedTextbook)}&node_id=` + selectedNode, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "ngrok-skip-browser-warning": "true",
      mode: "no-cors"
    }
  });
}

export const getNodes = async () => {
  const response = await fetch(localURL + "/get_textbook_graph?textbook_name=" + get(selectedTextbook), {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "ngrok-skip-browser-warning": "true",
      mode: "no-cors"
    }
  });
  const data = await response.json();
  console.log(data);
  const retrievedNodes : Node[] = data.nodes;
  const retrievedEdges : [number[]] = data.edges;

  let lowestUnfinished = Number.MAX_SAFE_INTEGER;
  retrievedNodes.forEach((node) => {
    if (node.completed == false && parseInt(node.group) < lowestUnfinished) {
      lowestUnfinished = parseInt(node.group);
    }
  });

  const newNode : Node[] = retrievedNodes.map((node) => {
    if (node.group == lowestUnfinished.toString()) {
      return {
        id: node.id,
        label: node.label,
        color: node.completed == true ? '#00E175' : '#FFFF00',
        group: node.group.toString(),
        completed: false
      }
    }
    else {
      return {
      id: node.id,
      label: node.label,
      color: node.completed == true ? '#00E175' : '#E10051',
      group: node.group.toString(),
    }
    }
    
  });
  const newEdges : Edge[] = retrievedEdges.map((edge) => {
    return {
      from: edge[0],
      to: edge[1]
    }
  })

  const parsedNames : string[] = [];
  retrievedNodes.forEach((node) => {
    parsedNames.push(node.label);
  });
  nodeNames.set(parsedNames);

  return {
    nodes: newNode,
    edges: newEdges
  }
};