<script lang="ts">

    import { onMount } from 'svelte';
    import { nodes, edges, selectedNode } from '$lib/api/nodes';
    import { blurred } from '$lib/api/chat';
    import { getNodes } from '$lib/api/nodes';
    import { Network, type AnimationOptions, type MoveToOptions } from 'vis-network';
    import { DataSet } from 'vis-data';

    let network;

    onMount(async () => {
        const container = document.getElementById("mynetwork");
        const backendData = await getNodes();
        if (container == null) {
            throw new Error("container is null");
        }
        const options = {
            layout: {
                improvedLayout: false,
            },
            nodes: {
              shape: "dot",
              size: 20,
            },
            physics: {
              forceAtlas2Based: {
                gravitationalConstant:-30,
                centralGravity: .0001,
                springLength: 230,
                springConstant: .10,
              },
              maxVelocity: 500,
              solver: "forceAtlas2Based",
              timestep: 0.25,
              stabilization: { iterations: 200 },
            },
        };

        const nodes = new DataSet<any>([backendData.nodes[0]]);
        const edges = new DataSet<any>([]);
        const data = {
            nodes: nodes,
            edges: edges,
        };
        network = new Network(container, data, options);
        

        network.once('stabilized', function() {
            var scaleOption = { scale : 0.1 };
            network.moveTo(scaleOption);
        });


        // network.moveTo({
        //     position: {x:0, y:0},    // position to animate to (Numbers)
        //     animation: {
        //         duration: 5000,
        //         easingFunction: "linear"
        //     },
        //     scale: 0.2,              // scale to animate to  (Number)
        // });
        
        // animate the nodes coming in
        for(let i = 0; i < backendData.nodes.length; i++) {
            // dynamically add nodes
            setTimeout(() => {
                nodes.add(backendData.nodes[i]);
                network.once('stabilized', function() {
                    var scaleOption = { scale : 0.1 };
                    network.moveTo(scaleOption);
                });
                // network.fit();
                // network.setSize('50wv', '100vh');

            }, i * 50);
        }
        
        // animate the edges coming in
        for(let i = 0; i < backendData.edges.length; i++) {
            // dynamically add edges
            setTimeout(() => {
                edges.add(backendData.edges[i]);
                // network.fit();
                
            }, i * 50);
        }

        // network.moveTo({
        //     position: {x:0, y:0},    // position to animate to (Numbers)
        //     animation: {
        //         duration: 15000,
        //         easingFunction: "linear"
        //     },
        //     scale: 0.2,              // scale to animate to  (Number)
        // });
       


        network.on('click', function (params) {
            console.log(params);
            if (params.nodes.length > 0) {
                if ($selectedNode != params.nodes[0])
                    selectedNode.set(params.nodes[0]);
                else {
                    blurred.set(true);
                }
            }
            else
                selectedNode.set(null);
        });
    });

</script>

<div id="mynetwork" />

<style>
    #mynetwork {
        width: 100vw;
        height: 70vh;
        position: fixed;
        top: 60%;
        left: 50%;
        transform: translate(-50%, -50%);
        /* border: 1px solid red; */
        margin-top: 55px;

        /* animation-name: grow;
        animation-duration: 15s;
        animation-iteration-count: 1; */
    }

    /* @keyframes grow {
        0%  {
            width: 50vw;
            height: 50vh;
        }
        25% {
            width: 70vw;
            height: 70vh;
        }
        50% {
            width: 85vw;
            height: 85vh;

        }
        100% {
            width: 100vw;
            height: 100vh;

        }
    } */

    :global(html) {
        overflow: hidden;
        padding: 0;
        margin: 0;
    }
</style>