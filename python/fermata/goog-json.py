



<!DOCTYPE html>
<html>
<head>
 <link rel="icon" type="image/vnd.microsoft.icon" href="http://www.gstatic.com/codesite/ph/images/phosting.ico">
 
 <script type="text/javascript">
 
 
 
 
 var codesite_token = "708e9ae8037a1f62ca964109d225650f";
 
 
 var CS_env = {"token":"708e9ae8037a1f62ca964109d225650f","assetHostPath":"http://www.gstatic.com/codesite/ph","domainName":null,"assetVersionPath":"http://www.gstatic.com/codesite/ph/12142458833428315778","projectName":"google-app-engine-samples","projectHomeUrl":"/p/google-app-engine-samples","absoluteBaseUrl":"http://code.google.com","relativeBaseUrl":"","urlPrefix":"p","loggedInUserEmail":"mattnashbrowns@gmail.com"};
 </script>
 
 
 <title>json.py - 
 google-app-engine-samples -
 
 
 Samples for Google App Engine - Google Project Hosting
 </title>
 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" >
 <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" >
 
 <meta name="ROBOTS" content="NOARCHIVE">
 
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/12142458833428315778/css/ph_core.css">
 
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/12142458833428315778/css/ph_detail.css" >
 
 
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/12142458833428315778/css/d_sb.css" >
 
 
 
<!--[if IE]>
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/12142458833428315778/css/d_ie.css" >
<![endif]-->
 <style type="text/css">
 .menuIcon.off { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 -42px }
 .menuIcon.on { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 -28px }
 .menuIcon.down { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 0; }
 
 
 
  tr.inline_comment {
 background: #fff;
 vertical-align: top;
 }
 div.draft, div.published {
 padding: .3em;
 border: 1px solid #999; 
 margin-bottom: .1em;
 font-family: arial, sans-serif;
 max-width: 60em;
 }
 div.draft {
 background: #ffa;
 } 
 div.published {
 background: #e5ecf9;
 }
 div.published .body, div.draft .body {
 padding: .5em .1em .1em .1em;
 max-width: 60em;
 white-space: pre-wrap;
 white-space: -moz-pre-wrap;
 white-space: -pre-wrap;
 white-space: -o-pre-wrap;
 word-wrap: break-word;
 font-size: 1em;
 }
 div.draft .actions {
 margin-left: 1em;
 font-size: 90%;
 }
 div.draft form {
 padding: .5em .5em .5em 0;
 }
 div.draft textarea, div.published textarea {
 width: 95%;
 height: 10em;
 font-family: arial, sans-serif;
 margin-bottom: .5em;
 }

 
 .nocursor, .nocursor td, .cursor_hidden, .cursor_hidden td {
 background-color: white;
 height: 2px;
 }
 .cursor, .cursor td {
 background-color: darkblue;
 height: 2px;
 display: '';
 }
 
 
.list {
 border: 1px solid white;
 border-bottom: 0;
}

 </style>
</head>
<body class="t4">
 <script type="text/javascript">
 var _gaq = _gaq || [];
 _gaq.push(
 ['siteTracker._setAccount', 'UA-18071-1'],
 ['siteTracker._trackPageview']);
 
 (function() {
 var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
 ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
 (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(ga);
 })();
 </script>
<div class="headbg">
 <div id="gaia">
 

 <span>
 
 
 <b>mattnashbrowns@gmail.com</b>
 
 
 | <a href="/u/@VhdeRFJQARhGWAJ0/" id="projects-dropdown" onclick="return false;"
 ><u>My favorites</u> <small>&#9660;</small></a>
 | <a href="/u/@VhdeRFJQARhGWAJ0/" onclick="_CS_click('/gb/ph/profile');" 
 title="Profile, Updates, and Settings"
 ><u>Profile</u></a>
 | <a href="https://www.google.com/accounts/Logout?continue=http%3A%2F%2Fcode.google.com%2Fp%2Fgoogle-app-engine-samples%2Fsource%2Fbrowse%2Ftrunk%2Fgeochat%2Fjson.py%3Fr%3D55" 
 onclick="_CS_click('/gb/ph/signout');"
 ><u>Sign out</u></a>
 
 </span>

 </div>
 <div class="gbh" style="left: 0pt;"></div>
 <div class="gbh" style="right: 0pt;"></div>
 
 
 <div style="height: 1px"></div>
<!--[if lte IE 7]>
<div style="text-align:center;">
Your version of Internet Explorer is not supported. Try a browser that
contributes to open source, such as <a href="http://www.firefox.com">Firefox</a>,
<a href="http://www.google.com/chrome">Google Chrome</a>, or
<a href="http://code.google.com/chrome/chromeframe/">Google Chrome Frame</a>.
</div>
<![endif]-->




 <table style="padding:0px; margin: 0px 0px 10px 0px; width:100%" cellpadding="0" cellspacing="0">
 <tr style="height: 58px;">
 
 <td id="plogo">
 <a href="/p/google-app-engine-samples/">
 
 <img src="http://www.gstatic.com/codesite/ph/images/search-48.gif" alt="Logo">
 
 </a>
 </td>
 
 <td style="padding-left: 0.5em">
 
 <div id="pname">
 <a href="/p/google-app-engine-samples/">google-app-engine-samples</a>
 </div>
 
 <div id="psum">
 <a id="project_summary_link" href="/p/google-app-engine-samples/" >Samples for Google App Engine</a>
 
 </div>
 
 
 </td>
 <td style="white-space:nowrap;text-align:right; vertical-align:bottom;">
 
 <form action="/hosting/search">
 <input size="30" name="q" value="" type="text">
 <input type="submit" name="projectsearch" value="Search projects" >
 </form>
 
 </tr>
 </table>

</div>

 
<div id="mt" class="gtb"> 
 <a href="/p/google-app-engine-samples/" class="tab ">Project&nbsp;Home</a>
 
 
 
 
 <a href="/p/google-app-engine-samples/downloads/list" class="tab ">Downloads</a>
 
 
 
 
 
 <a href="/p/google-app-engine-samples/w/list" class="tab ">Wiki</a>
 
 
 
 
 
 <a href="/p/google-app-engine-samples/issues/list"
 class="tab ">Issues</a>
 
 
 
 
 
 <a href="/p/google-app-engine-samples/source/checkout"
 class="tab active">Source</a>
 
 
 
 
 
 <div class=gtbc></div>
</div>
<table cellspacing="0" cellpadding="0" width="100%" align="center" border="0" class="st">
 <tr>
 
 
 
 
 
 
 <td class="subt">
 <div class="st2">
 <div class="isf">
 
 
 
 <span class="inst1"><a href="/p/google-app-engine-samples/source/checkout">Checkout</a></span> &nbsp;
 <span class="inst2"><a href="/p/google-app-engine-samples/source/browse/">Browse</a></span> &nbsp;
 <span class="inst3"><a href="/p/google-app-engine-samples/source/list">Changes</a></span> &nbsp;
 
 <form action="http://www.google.com/codesearch" method="get" style="display:inline"
 onsubmit="document.getElementById('codesearchq').value = document.getElementById('origq').value + ' package:http://google-app-engine-samples\\.googlecode\\.com'">
 <input type="hidden" name="q" id="codesearchq" value="">
 <input type="text" maxlength="2048" size="38" id="origq" name="origq" value="" title="Google Code Search" style="font-size:92%">&nbsp;<input type="submit" value="Search Trunk" name="btnG" style="font-size:92%">
 
 
 
 </form>
 </div>
</div>

 </td>
 
 
 
 <td align="right" valign="top" class="bevel-right"></td>
 </tr>
</table>


<script type="text/javascript">
 var cancelBubble = false;
 function _go(url) { document.location = url; }
</script>
<div id="maincol"
 
>

 
<!-- IE -->




<div class="collapse">
<div id="colcontrol">
<style type="text/css">
 #file_flipper { white-space: nowrap; padding-right: 2em; }
 #file_flipper.hidden { display: none; }
 #file_flipper .pagelink { color: #0000CC; text-decoration: underline; }
 #file_flipper #visiblefiles { padding-left: 0.5em; padding-right: 0.5em; }
</style>
<table id="nav_and_rev" class="list"
 cellpadding="0" cellspacing="0" width="100%">
 <tr>
 
 <td nowrap="nowrap" class="src_crumbs src_nav" width="33%">
 <strong class="src_nav">Source path:&nbsp;</strong>
 <span id="crumb_root">
 
 <a href="/p/google-app-engine-samples/source/browse/?r=55">svn</a>/&nbsp;</span>
 <span id="crumb_links" class="ifClosed"><a href="/p/google-app-engine-samples/source/browse/trunk/?r=55">trunk</a><span class="sp">/&nbsp;</span><a href="/p/google-app-engine-samples/source/browse/trunk/geochat/?r=55">geochat</a><span class="sp">/&nbsp;</span>json.py</span>
 
 

 </td>
 
 
 <td nowrap="nowrap" width="33%" align="right">
 <table cellpadding="0" cellspacing="0" style="font-size: 100%"><tr>
 
 
 <td class="flipper"><b>r55</b></td>
 
 </tr></table>
 </td> 
 </tr>
</table>

<div class="fc">
 
 
 
<style type="text/css">
.undermouse span {
 background-image: url(http://www.gstatic.com/codesite/ph/images/comments.gif); }
</style>
<table class="opened" id="review_comment_area"
><tr>
<td id="nums">
<pre><table width="100%"><tr class="nocursor"><td></td></tr></table></pre>
<pre><table width="100%" id="nums_table_0"><tr id="gr_svn55_1"

><td id="1"><a href="#1">1</a></td></tr
><tr id="gr_svn55_2"

><td id="2"><a href="#2">2</a></td></tr
><tr id="gr_svn55_3"

><td id="3"><a href="#3">3</a></td></tr
><tr id="gr_svn55_4"

><td id="4"><a href="#4">4</a></td></tr
><tr id="gr_svn55_5"

><td id="5"><a href="#5">5</a></td></tr
><tr id="gr_svn55_6"

><td id="6"><a href="#6">6</a></td></tr
><tr id="gr_svn55_7"

><td id="7"><a href="#7">7</a></td></tr
><tr id="gr_svn55_8"

><td id="8"><a href="#8">8</a></td></tr
><tr id="gr_svn55_9"

><td id="9"><a href="#9">9</a></td></tr
><tr id="gr_svn55_10"

><td id="10"><a href="#10">10</a></td></tr
><tr id="gr_svn55_11"

><td id="11"><a href="#11">11</a></td></tr
><tr id="gr_svn55_12"

><td id="12"><a href="#12">12</a></td></tr
><tr id="gr_svn55_13"

><td id="13"><a href="#13">13</a></td></tr
><tr id="gr_svn55_14"

><td id="14"><a href="#14">14</a></td></tr
><tr id="gr_svn55_15"

><td id="15"><a href="#15">15</a></td></tr
><tr id="gr_svn55_16"

><td id="16"><a href="#16">16</a></td></tr
><tr id="gr_svn55_17"

><td id="17"><a href="#17">17</a></td></tr
><tr id="gr_svn55_18"

><td id="18"><a href="#18">18</a></td></tr
><tr id="gr_svn55_19"

><td id="19"><a href="#19">19</a></td></tr
><tr id="gr_svn55_20"

><td id="20"><a href="#20">20</a></td></tr
><tr id="gr_svn55_21"

><td id="21"><a href="#21">21</a></td></tr
><tr id="gr_svn55_22"

><td id="22"><a href="#22">22</a></td></tr
><tr id="gr_svn55_23"

><td id="23"><a href="#23">23</a></td></tr
><tr id="gr_svn55_24"

><td id="24"><a href="#24">24</a></td></tr
><tr id="gr_svn55_25"

><td id="25"><a href="#25">25</a></td></tr
><tr id="gr_svn55_26"

><td id="26"><a href="#26">26</a></td></tr
><tr id="gr_svn55_27"

><td id="27"><a href="#27">27</a></td></tr
><tr id="gr_svn55_28"

><td id="28"><a href="#28">28</a></td></tr
><tr id="gr_svn55_29"

><td id="29"><a href="#29">29</a></td></tr
><tr id="gr_svn55_30"

><td id="30"><a href="#30">30</a></td></tr
><tr id="gr_svn55_31"

><td id="31"><a href="#31">31</a></td></tr
><tr id="gr_svn55_32"

><td id="32"><a href="#32">32</a></td></tr
><tr id="gr_svn55_33"

><td id="33"><a href="#33">33</a></td></tr
><tr id="gr_svn55_34"

><td id="34"><a href="#34">34</a></td></tr
><tr id="gr_svn55_35"

><td id="35"><a href="#35">35</a></td></tr
><tr id="gr_svn55_36"

><td id="36"><a href="#36">36</a></td></tr
><tr id="gr_svn55_37"

><td id="37"><a href="#37">37</a></td></tr
><tr id="gr_svn55_38"

><td id="38"><a href="#38">38</a></td></tr
><tr id="gr_svn55_39"

><td id="39"><a href="#39">39</a></td></tr
><tr id="gr_svn55_40"

><td id="40"><a href="#40">40</a></td></tr
><tr id="gr_svn55_41"

><td id="41"><a href="#41">41</a></td></tr
><tr id="gr_svn55_42"

><td id="42"><a href="#42">42</a></td></tr
><tr id="gr_svn55_43"

><td id="43"><a href="#43">43</a></td></tr
><tr id="gr_svn55_44"

><td id="44"><a href="#44">44</a></td></tr
><tr id="gr_svn55_45"

><td id="45"><a href="#45">45</a></td></tr
><tr id="gr_svn55_46"

><td id="46"><a href="#46">46</a></td></tr
><tr id="gr_svn55_47"

><td id="47"><a href="#47">47</a></td></tr
><tr id="gr_svn55_48"

><td id="48"><a href="#48">48</a></td></tr
><tr id="gr_svn55_49"

><td id="49"><a href="#49">49</a></td></tr
><tr id="gr_svn55_50"

><td id="50"><a href="#50">50</a></td></tr
><tr id="gr_svn55_51"

><td id="51"><a href="#51">51</a></td></tr
><tr id="gr_svn55_52"

><td id="52"><a href="#52">52</a></td></tr
><tr id="gr_svn55_53"

><td id="53"><a href="#53">53</a></td></tr
><tr id="gr_svn55_54"

><td id="54"><a href="#54">54</a></td></tr
><tr id="gr_svn55_55"

><td id="55"><a href="#55">55</a></td></tr
><tr id="gr_svn55_56"

><td id="56"><a href="#56">56</a></td></tr
><tr id="gr_svn55_57"

><td id="57"><a href="#57">57</a></td></tr
><tr id="gr_svn55_58"

><td id="58"><a href="#58">58</a></td></tr
><tr id="gr_svn55_59"

><td id="59"><a href="#59">59</a></td></tr
><tr id="gr_svn55_60"

><td id="60"><a href="#60">60</a></td></tr
><tr id="gr_svn55_61"

><td id="61"><a href="#61">61</a></td></tr
><tr id="gr_svn55_62"

><td id="62"><a href="#62">62</a></td></tr
><tr id="gr_svn55_63"

><td id="63"><a href="#63">63</a></td></tr
><tr id="gr_svn55_64"

><td id="64"><a href="#64">64</a></td></tr
><tr id="gr_svn55_65"

><td id="65"><a href="#65">65</a></td></tr
><tr id="gr_svn55_66"

><td id="66"><a href="#66">66</a></td></tr
><tr id="gr_svn55_67"

><td id="67"><a href="#67">67</a></td></tr
><tr id="gr_svn55_68"

><td id="68"><a href="#68">68</a></td></tr
><tr id="gr_svn55_69"

><td id="69"><a href="#69">69</a></td></tr
><tr id="gr_svn55_70"

><td id="70"><a href="#70">70</a></td></tr
><tr id="gr_svn55_71"

><td id="71"><a href="#71">71</a></td></tr
><tr id="gr_svn55_72"

><td id="72"><a href="#72">72</a></td></tr
><tr id="gr_svn55_73"

><td id="73"><a href="#73">73</a></td></tr
><tr id="gr_svn55_74"

><td id="74"><a href="#74">74</a></td></tr
><tr id="gr_svn55_75"

><td id="75"><a href="#75">75</a></td></tr
><tr id="gr_svn55_76"

><td id="76"><a href="#76">76</a></td></tr
><tr id="gr_svn55_77"

><td id="77"><a href="#77">77</a></td></tr
><tr id="gr_svn55_78"

><td id="78"><a href="#78">78</a></td></tr
><tr id="gr_svn55_79"

><td id="79"><a href="#79">79</a></td></tr
><tr id="gr_svn55_80"

><td id="80"><a href="#80">80</a></td></tr
><tr id="gr_svn55_81"

><td id="81"><a href="#81">81</a></td></tr
><tr id="gr_svn55_82"

><td id="82"><a href="#82">82</a></td></tr
><tr id="gr_svn55_83"

><td id="83"><a href="#83">83</a></td></tr
><tr id="gr_svn55_84"

><td id="84"><a href="#84">84</a></td></tr
><tr id="gr_svn55_85"

><td id="85"><a href="#85">85</a></td></tr
><tr id="gr_svn55_86"

><td id="86"><a href="#86">86</a></td></tr
><tr id="gr_svn55_87"

><td id="87"><a href="#87">87</a></td></tr
><tr id="gr_svn55_88"

><td id="88"><a href="#88">88</a></td></tr
><tr id="gr_svn55_89"

><td id="89"><a href="#89">89</a></td></tr
><tr id="gr_svn55_90"

><td id="90"><a href="#90">90</a></td></tr
><tr id="gr_svn55_91"

><td id="91"><a href="#91">91</a></td></tr
><tr id="gr_svn55_92"

><td id="92"><a href="#92">92</a></td></tr
><tr id="gr_svn55_93"

><td id="93"><a href="#93">93</a></td></tr
><tr id="gr_svn55_94"

><td id="94"><a href="#94">94</a></td></tr
><tr id="gr_svn55_95"

><td id="95"><a href="#95">95</a></td></tr
><tr id="gr_svn55_96"

><td id="96"><a href="#96">96</a></td></tr
><tr id="gr_svn55_97"

><td id="97"><a href="#97">97</a></td></tr
><tr id="gr_svn55_98"

><td id="98"><a href="#98">98</a></td></tr
><tr id="gr_svn55_99"

><td id="99"><a href="#99">99</a></td></tr
><tr id="gr_svn55_100"

><td id="100"><a href="#100">100</a></td></tr
><tr id="gr_svn55_101"

><td id="101"><a href="#101">101</a></td></tr
></table></pre>
<pre><table width="100%"><tr class="nocursor"><td></td></tr></table></pre>
</td>
<td id="lines">
<pre><table width="100%"><tr class="cursor_stop cursor_hidden"><td></td></tr></table></pre>
<pre class="prettyprint lang-py"><table id="src_table_0"><tr
id=sl_svn55_1

><td class="source"><br></td></tr
><tr
id=sl_svn55_2

><td class="source"># Copyright 2008 Google Inc.<br></td></tr
><tr
id=sl_svn55_3

><td class="source">#<br></td></tr
><tr
id=sl_svn55_4

><td class="source"># Licensed under the Apache License, Version 2.0 (the &quot;License&quot;);<br></td></tr
><tr
id=sl_svn55_5

><td class="source"># you may not use this file except in compliance with the License.<br></td></tr
><tr
id=sl_svn55_6

><td class="source"># You may obtain a copy of the License at<br></td></tr
><tr
id=sl_svn55_7

><td class="source"># <br></td></tr
><tr
id=sl_svn55_8

><td class="source">#     http://www.apache.org/licenses/LICENSE-2.0<br></td></tr
><tr
id=sl_svn55_9

><td class="source"># <br></td></tr
><tr
id=sl_svn55_10

><td class="source"># Unless required by applicable law or agreed to in writing, software<br></td></tr
><tr
id=sl_svn55_11

><td class="source"># distributed under the License is distributed on an &quot;AS IS&quot; BASIS,<br></td></tr
><tr
id=sl_svn55_12

><td class="source"># WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.<br></td></tr
><tr
id=sl_svn55_13

><td class="source"># See the License for the specific language governing permissions and<br></td></tr
><tr
id=sl_svn55_14

><td class="source"># limitations under the License.<br></td></tr
><tr
id=sl_svn55_15

><td class="source"><br></td></tr
><tr
id=sl_svn55_16

><td class="source">&quot;&quot;&quot;Utility classes and methods for use with simplejson and appengine.<br></td></tr
><tr
id=sl_svn55_17

><td class="source"><br></td></tr
><tr
id=sl_svn55_18

><td class="source">Provides both a specialized simplejson encoder, GqlEncoder, designed to simplify<br></td></tr
><tr
id=sl_svn55_19

><td class="source">encoding directly from GQL results to JSON. A helper function, encode, is also<br></td></tr
><tr
id=sl_svn55_20

><td class="source">provided to further simplify usage.<br></td></tr
><tr
id=sl_svn55_21

><td class="source"><br></td></tr
><tr
id=sl_svn55_22

><td class="source">  GqlEncoder: Adds support for GQL results and properties to simplejson.<br></td></tr
><tr
id=sl_svn55_23

><td class="source">  encode(input): Direct method to encode GQL objects as JSON.<br></td></tr
><tr
id=sl_svn55_24

><td class="source">&quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn55_25

><td class="source"><br></td></tr
><tr
id=sl_svn55_26

><td class="source">import datetime<br></td></tr
><tr
id=sl_svn55_27

><td class="source">import simplejson<br></td></tr
><tr
id=sl_svn55_28

><td class="source">import time<br></td></tr
><tr
id=sl_svn55_29

><td class="source"><br></td></tr
><tr
id=sl_svn55_30

><td class="source">from google.appengine.api import users<br></td></tr
><tr
id=sl_svn55_31

><td class="source">from google.appengine.ext import db<br></td></tr
><tr
id=sl_svn55_32

><td class="source"><br></td></tr
><tr
id=sl_svn55_33

><td class="source"><br></td></tr
><tr
id=sl_svn55_34

><td class="source">class GqlEncoder(simplejson.JSONEncoder):<br></td></tr
><tr
id=sl_svn55_35

><td class="source">  <br></td></tr
><tr
id=sl_svn55_36

><td class="source">  &quot;&quot;&quot;Extends JSONEncoder to add support for GQL results and properties.<br></td></tr
><tr
id=sl_svn55_37

><td class="source">  <br></td></tr
><tr
id=sl_svn55_38

><td class="source">  Adds support to simplejson JSONEncoders for GQL results and properties by<br></td></tr
><tr
id=sl_svn55_39

><td class="source">  overriding JSONEncoder&#39;s default method.<br></td></tr
><tr
id=sl_svn55_40

><td class="source">  &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn55_41

><td class="source">  <br></td></tr
><tr
id=sl_svn55_42

><td class="source">  # TODO Improve coverage for all of App Engine&#39;s Property types.<br></td></tr
><tr
id=sl_svn55_43

><td class="source"><br></td></tr
><tr
id=sl_svn55_44

><td class="source">  def default(self, obj):<br></td></tr
><tr
id=sl_svn55_45

><td class="source">    <br></td></tr
><tr
id=sl_svn55_46

><td class="source">    &quot;&quot;&quot;Tests the input object, obj, to encode as JSON.&quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn55_47

><td class="source"><br></td></tr
><tr
id=sl_svn55_48

><td class="source">    if hasattr(obj, &#39;__json__&#39;):<br></td></tr
><tr
id=sl_svn55_49

><td class="source">      return getattr(obj, &#39;__json__&#39;)()<br></td></tr
><tr
id=sl_svn55_50

><td class="source"><br></td></tr
><tr
id=sl_svn55_51

><td class="source">    if isinstance(obj, db.GqlQuery):<br></td></tr
><tr
id=sl_svn55_52

><td class="source">      return list(obj)<br></td></tr
><tr
id=sl_svn55_53

><td class="source"><br></td></tr
><tr
id=sl_svn55_54

><td class="source">    elif isinstance(obj, db.Model):<br></td></tr
><tr
id=sl_svn55_55

><td class="source">      properties = obj.properties().items()<br></td></tr
><tr
id=sl_svn55_56

><td class="source">      output = {}<br></td></tr
><tr
id=sl_svn55_57

><td class="source">      for field, value in properties:<br></td></tr
><tr
id=sl_svn55_58

><td class="source">        output[field] = getattr(obj, field)<br></td></tr
><tr
id=sl_svn55_59

><td class="source">      return output<br></td></tr
><tr
id=sl_svn55_60

><td class="source"><br></td></tr
><tr
id=sl_svn55_61

><td class="source">    elif isinstance(obj, datetime.datetime):<br></td></tr
><tr
id=sl_svn55_62

><td class="source">      output = {}<br></td></tr
><tr
id=sl_svn55_63

><td class="source">      fields = [&#39;day&#39;, &#39;hour&#39;, &#39;microsecond&#39;, &#39;minute&#39;, &#39;month&#39;, &#39;second&#39;,<br></td></tr
><tr
id=sl_svn55_64

><td class="source">          &#39;year&#39;]<br></td></tr
><tr
id=sl_svn55_65

><td class="source">      methods = [&#39;ctime&#39;, &#39;isocalendar&#39;, &#39;isoformat&#39;, &#39;isoweekday&#39;,<br></td></tr
><tr
id=sl_svn55_66

><td class="source">          &#39;timetuple&#39;]<br></td></tr
><tr
id=sl_svn55_67

><td class="source">      for field in fields:<br></td></tr
><tr
id=sl_svn55_68

><td class="source">        output[field] = getattr(obj, field)<br></td></tr
><tr
id=sl_svn55_69

><td class="source">      for method in methods:<br></td></tr
><tr
id=sl_svn55_70

><td class="source">        output[method] = getattr(obj, method)()<br></td></tr
><tr
id=sl_svn55_71

><td class="source">      output[&#39;epoch&#39;] = time.mktime(obj.timetuple())<br></td></tr
><tr
id=sl_svn55_72

><td class="source">      return output<br></td></tr
><tr
id=sl_svn55_73

><td class="source"><br></td></tr
><tr
id=sl_svn55_74

><td class="source">    elif isinstance(obj, time.struct_time):<br></td></tr
><tr
id=sl_svn55_75

><td class="source">      return list(obj)<br></td></tr
><tr
id=sl_svn55_76

><td class="source"><br></td></tr
><tr
id=sl_svn55_77

><td class="source">    elif isinstance(obj, users.User):<br></td></tr
><tr
id=sl_svn55_78

><td class="source">      output = {}<br></td></tr
><tr
id=sl_svn55_79

><td class="source">      methods = [&#39;nickname&#39;, &#39;email&#39;, &#39;auth_domain&#39;]<br></td></tr
><tr
id=sl_svn55_80

><td class="source">      for method in methods:<br></td></tr
><tr
id=sl_svn55_81

><td class="source">        output[method] = getattr(obj, method)()<br></td></tr
><tr
id=sl_svn55_82

><td class="source">      return output<br></td></tr
><tr
id=sl_svn55_83

><td class="source"><br></td></tr
><tr
id=sl_svn55_84

><td class="source">    return simplejson.JSONEncoder.default(self, obj)<br></td></tr
><tr
id=sl_svn55_85

><td class="source"><br></td></tr
><tr
id=sl_svn55_86

><td class="source"><br></td></tr
><tr
id=sl_svn55_87

><td class="source">def encode(input):<br></td></tr
><tr
id=sl_svn55_88

><td class="source">  &quot;&quot;&quot;Encode an input GQL object as JSON<br></td></tr
><tr
id=sl_svn55_89

><td class="source"><br></td></tr
><tr
id=sl_svn55_90

><td class="source">    Args:<br></td></tr
><tr
id=sl_svn55_91

><td class="source">      input: A GQL object or DB property.<br></td></tr
><tr
id=sl_svn55_92

><td class="source"><br></td></tr
><tr
id=sl_svn55_93

><td class="source">    Returns:<br></td></tr
><tr
id=sl_svn55_94

><td class="source">      A JSON string based on the input object. <br></td></tr
><tr
id=sl_svn55_95

><td class="source">      <br></td></tr
><tr
id=sl_svn55_96

><td class="source">    Raises:<br></td></tr
><tr
id=sl_svn55_97

><td class="source">      TypeError: Typically occurs when an input object contains an unsupported<br></td></tr
><tr
id=sl_svn55_98

><td class="source">        type.<br></td></tr
><tr
id=sl_svn55_99

><td class="source">    &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn55_100

><td class="source">  return GqlEncoder().encode(input)  <br></td></tr
><tr
id=sl_svn55_101

><td class="source"><br></td></tr
></table></pre>
<pre><table width="100%"><tr class="cursor_stop cursor_hidden"><td></td></tr></table></pre>
</td>
</tr></table>

 
<script type="text/javascript">
 var lineNumUnderMouse = -1;
 
 function gutterOver(num) {
 gutterOut();
 var newTR = document.getElementById('gr_svn55_' + num);
 if (newTR) {
 newTR.className = 'undermouse';
 }
 lineNumUnderMouse = num;
 }
 function gutterOut() {
 if (lineNumUnderMouse != -1) {
 var oldTR = document.getElementById(
 'gr_svn55_' + lineNumUnderMouse);
 if (oldTR) {
 oldTR.className = '';
 }
 lineNumUnderMouse = -1;
 }
 }
 var numsGenState = {table_base_id: 'nums_table_'};
 var srcGenState = {table_base_id: 'src_table_'};
 var alignerRunning = false;
 var startOver = false;
 function setLineNumberHeights() {
 if (alignerRunning) {
 startOver = true;
 return;
 }
 numsGenState.chunk_id = 0;
 numsGenState.table = document.getElementById('nums_table_0');
 numsGenState.row_num = 0;
 if (!numsGenState.table) {
 return; // Silently exit if no file is present.
 }
 srcGenState.chunk_id = 0;
 srcGenState.table = document.getElementById('src_table_0');
 srcGenState.row_num = 0;
 alignerRunning = true;
 continueToSetLineNumberHeights();
 }
 function rowGenerator(genState) {
 if (genState.row_num < genState.table.rows.length) {
 var currentRow = genState.table.rows[genState.row_num];
 genState.row_num++;
 return currentRow;
 }
 var newTable = document.getElementById(
 genState.table_base_id + (genState.chunk_id + 1));
 if (newTable) {
 genState.chunk_id++;
 genState.row_num = 0;
 genState.table = newTable;
 return genState.table.rows[0];
 }
 return null;
 }
 var MAX_ROWS_PER_PASS = 1000;
 function continueToSetLineNumberHeights() {
 var rowsInThisPass = 0;
 var numRow = 1;
 var srcRow = 1;
 while (numRow && srcRow && rowsInThisPass < MAX_ROWS_PER_PASS) {
 numRow = rowGenerator(numsGenState);
 srcRow = rowGenerator(srcGenState);
 rowsInThisPass++;
 if (numRow && srcRow) {
 if (numRow.offsetHeight != srcRow.offsetHeight) {
 numRow.firstChild.style.height = srcRow.offsetHeight + 'px';
 }
 }
 }
 if (rowsInThisPass >= MAX_ROWS_PER_PASS) {
 setTimeout(continueToSetLineNumberHeights, 10);
 } else {
 alignerRunning = false;
 if (startOver) {
 startOver = false;
 setTimeout(setLineNumberHeights, 500);
 }
 }
 }
 function initLineNumberHeights() {
 // Do 2 complete passes, because there can be races
 // between this code and prettify.
 startOver = true;
 setTimeout(setLineNumberHeights, 250);
 window.onresize = setLineNumberHeights;
 }
 initLineNumberHeights();
</script>

 
 
 <div id="log">
 <div style="text-align:right">
 <a class="ifCollapse" href="#" onclick="_toggleMeta('', 'p', 'google-app-engine-samples', this)">Show details</a>
 <a class="ifExpand" href="#" onclick="_toggleMeta('', 'p', 'google-app-engine-samples', this)">Hide details</a>
 </div>
 <div class="ifExpand">
 
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="changelog">
 <p>Change log</p>
 <div>
 <a href="/p/google-app-engine-samples/source/detail?spec=svn55&r=19">r19</a>
 by d...@google.com
 on Apr 9, 2008
 &nbsp; <a href="/p/google-app-engine-samples/source/diff?spec=svn55&r=19&amp;format=side&amp;path=/trunk/geochat/json.py&amp;old_path=/trunk/geochat/json.py&amp;old=">Diff</a>
 </div>
 <pre>Added</pre>
 </div>
 
 
 
 
 
 
 <script type="text/javascript">
 var detail_url = '/p/google-app-engine-samples/source/detail?r=19&spec=svn55';
 var publish_url = '/p/google-app-engine-samples/source/detail?r=19&spec=svn55#publish';
 // describe the paths of this revision in javascript.
 var changed_paths = [];
 var changed_urls = [];
 
 changed_paths.push('/trunk/geochat');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/LICENSE');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/LICENSE?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/README');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/README?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/app.yaml');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/app.yaml?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/chat.pyc');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/chat.pyc?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/datamodel.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/datamodel.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/datamodel.pyc');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/datamodel.pyc?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/events.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/events.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/geochat.html');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/geochat.html?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/geochat.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/geochat.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/help.html');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/help.html?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/index.yaml');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/index.yaml?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/json.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/json.py?r\x3d19\x26spec\x3dsvn55');
 
 var selected_path = '/trunk/geochat/json.py';
 
 
 changed_paths.push('/trunk/geochat/json.pyc');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/json.pyc?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/move.pyc');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/move.pyc?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/settings.html');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/settings.html?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/settings.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/settings.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/settings.pyc');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/settings.pyc?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/__init__.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/__init__.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/__init__.pyc');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/__init__.pyc?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/_speedups.c');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/_speedups.c?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/decoder.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/decoder.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/decoder.pyc');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/decoder.pyc?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/encoder.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/encoder.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/encoder.pyc');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/encoder.pyc?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/jsonfilter.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/jsonfilter.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/scanner.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/scanner.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/scanner.pyc');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/scanner.pyc?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/__init__.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/__init__.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/test_attacks.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_attacks.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/test_dump.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_dump.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/test_fail.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_fail.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/test_float.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_float.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/test_indent.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_indent.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/test_pass1.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_pass1.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/test_pass2.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_pass2.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/test_pass3.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_pass3.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/test_recursion.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_recursion.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/test_separators.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_separators.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/simplejson/tests/test_unicode.py');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_unicode.py?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/static');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/static?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/static/css');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/static/css?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/static/css/geochat.css');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/static/css/geochat.css?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/static/html');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/static/html?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/static/html/.prototype.html.swp');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/static/html/.prototype.html.swp?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/static/images');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/static/images?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/static/images/bubble-bg-bottom.png');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/static/images/bubble-bg-bottom.png?r\x3d19\x26spec\x3dsvn55');
 
 
 changed_paths.push('/trunk/geochat/static/images/bubble-bg-middle.png');
 changed_urls.push('/p/google-app-engine-samples/source/browse/trunk/geochat/static/images/bubble-bg-middle.png?r\x3d19\x26spec\x3dsvn55');
 
 
 function getCurrentPageIndex() {
 for (var i = 0; i < changed_paths.length; i++) {
 if (selected_path == changed_paths[i]) {
 return i;
 }
 }
 }
 function getNextPage() {
 var i = getCurrentPageIndex();
 if (i < changed_paths.length - 1) {
 return changed_urls[i + 1];
 }
 return null;
 }
 function getPreviousPage() {
 var i = getCurrentPageIndex();
 if (i > 0) {
 return changed_urls[i - 1];
 }
 return null;
 }
 function gotoNextPage() {
 var page = getNextPage();
 if (!page) {
 page = detail_url;
 }
 window.location = page;
 }
 function gotoPreviousPage() {
 var page = getPreviousPage();
 if (!page) {
 page = detail_url;
 }
 window.location = page;
 }
 function gotoDetailPage() {
 window.location = detail_url;
 }
 function gotoPublishPage() {
 window.location = publish_url;
 }
</script>

 
 <style type="text/css">
 #review_nav {
 border-top: 3px solid white;
 padding-top: 6px;
 margin-top: 1em;
 }
 #review_nav td {
 vertical-align: middle;
 }
 #review_nav select {
 margin: .5em 0;
 }
 </style>
 <div id="review_nav">
 <table><tr><td>Go to:&nbsp;</td><td>
 <select name="files_in_rev" onchange="window.location=this.value">
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat?r=19&amp;spec=svn55"
 
 >/trunk/geochat</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/LICENSE?r=19&amp;spec=svn55"
 
 >/trunk/geochat/LICENSE</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/README?r=19&amp;spec=svn55"
 
 >/trunk/geochat/README</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/app.yaml?r=19&amp;spec=svn55"
 
 >/trunk/geochat/app.yaml</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/chat.pyc?r=19&amp;spec=svn55"
 
 >/trunk/geochat/chat.pyc</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/datamodel.py?r=19&amp;spec=svn55"
 
 >/trunk/geochat/datamodel.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/datamodel.pyc?r=19&amp;spec=svn55"
 
 >/trunk/geochat/datamodel.pyc</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/events.py?r=19&amp;spec=svn55"
 
 >/trunk/geochat/events.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/geochat.html?r=19&amp;spec=svn55"
 
 >/trunk/geochat/geochat.html</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/geochat.py?r=19&amp;spec=svn55"
 
 >/trunk/geochat/geochat.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/help.html?r=19&amp;spec=svn55"
 
 >/trunk/geochat/help.html</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/index.yaml?r=19&amp;spec=svn55"
 
 >/trunk/geochat/index.yaml</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/json.py?r=19&amp;spec=svn55"
 selected="selected"
 >/trunk/geochat/json.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/json.pyc?r=19&amp;spec=svn55"
 
 >/trunk/geochat/json.pyc</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/move.pyc?r=19&amp;spec=svn55"
 
 >/trunk/geochat/move.pyc</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/settings.html?r=19&amp;spec=svn55"
 
 >/trunk/geochat/settings.html</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/settings.py?r=19&amp;spec=svn55"
 
 >/trunk/geochat/settings.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/settings.pyc?r=19&amp;spec=svn55"
 
 >/trunk/geochat/settings.pyc</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson?r=19&amp;spec=svn55"
 
 >/trunk/geochat/simplejson</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/__init__.py?r=19&amp;spec=svn55"
 
 >...k/geochat/simplejson/__init__.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/__init__.pyc?r=19&amp;spec=svn55"
 
 >.../geochat/simplejson/__init__.pyc</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/_speedups.c?r=19&amp;spec=svn55"
 
 >...k/geochat/simplejson/_speedups.c</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/decoder.py?r=19&amp;spec=svn55"
 
 >...nk/geochat/simplejson/decoder.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/decoder.pyc?r=19&amp;spec=svn55"
 
 >...k/geochat/simplejson/decoder.pyc</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/encoder.py?r=19&amp;spec=svn55"
 
 >...nk/geochat/simplejson/encoder.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/encoder.pyc?r=19&amp;spec=svn55"
 
 >...k/geochat/simplejson/encoder.pyc</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/jsonfilter.py?r=19&amp;spec=svn55"
 
 >...geochat/simplejson/jsonfilter.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/scanner.py?r=19&amp;spec=svn55"
 
 >...nk/geochat/simplejson/scanner.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/scanner.pyc?r=19&amp;spec=svn55"
 
 >...k/geochat/simplejson/scanner.pyc</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests?r=19&amp;spec=svn55"
 
 >/trunk/geochat/simplejson/tests</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/__init__.py?r=19&amp;spec=svn55"
 
 >...hat/simplejson/tests/__init__.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_attacks.py?r=19&amp;spec=svn55"
 
 >...simplejson/tests/test_attacks.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_dump.py?r=19&amp;spec=svn55"
 
 >...at/simplejson/tests/test_dump.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_fail.py?r=19&amp;spec=svn55"
 
 >...at/simplejson/tests/test_fail.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_float.py?r=19&amp;spec=svn55"
 
 >...t/simplejson/tests/test_float.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_indent.py?r=19&amp;spec=svn55"
 
 >.../simplejson/tests/test_indent.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_pass1.py?r=19&amp;spec=svn55"
 
 >...t/simplejson/tests/test_pass1.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_pass2.py?r=19&amp;spec=svn55"
 
 >...t/simplejson/tests/test_pass2.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_pass3.py?r=19&amp;spec=svn55"
 
 >...t/simplejson/tests/test_pass3.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_recursion.py?r=19&amp;spec=svn55"
 
 >...mplejson/tests/test_recursion.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_separators.py?r=19&amp;spec=svn55"
 
 >...plejson/tests/test_separators.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/simplejson/tests/test_unicode.py?r=19&amp;spec=svn55"
 
 >...simplejson/tests/test_unicode.py</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/static?r=19&amp;spec=svn55"
 
 >/trunk/geochat/static</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/static/css?r=19&amp;spec=svn55"
 
 >/trunk/geochat/static/css</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/static/css/geochat.css?r=19&amp;spec=svn55"
 
 >...k/geochat/static/css/geochat.css</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/static/html?r=19&amp;spec=svn55"
 
 >/trunk/geochat/static/html</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/static/html/.prototype.html.swp?r=19&amp;spec=svn55"
 
 >.../static/html/.prototype.html.swp</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/static/images?r=19&amp;spec=svn55"
 
 >/trunk/geochat/static/images</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/static/images/bubble-bg-bottom.png?r=19&amp;spec=svn55"
 
 >...atic/images/bubble-bg-bottom.png</option>
 
 <option value="/p/google-app-engine-samples/source/browse/trunk/geochat/static/images/bubble-bg-middle.png?r=19&amp;spec=svn55"
 
 >...atic/images/bubble-bg-middle.png</option>
 
 </select>
 </td></tr></table>
 
 <div id="review_show_hide" class="opened">
 <div class="ifOpened"><a href="#" onclick="return toggleComments()">Hide comments</a></div>
 <div class="ifClosed"><a href="#" onclick="return toggleComments()">Show comments</a></div>
 </div>
 
 
 



 
 </div>
 
 
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="older_bubble">
 <p>Older revisions</p>
 
 <a href="/p/google-app-engine-samples/source/list?path=/trunk/geochat/json.py&start=19">All revisions of this file</a>
 </div>
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="fileinfo_bubble">
 <p>File info</p>
 
 <div>Size: 2984 bytes,
 101 lines</div>
 
 <div><a href="//google-app-engine-samples.googlecode.com/svn-history/r55/trunk/geochat/json.py">View raw file</a></div>
 </div>
 
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 </div>
 </div>


</div>

</div>
</div>

<script src="http://www.gstatic.com/codesite/ph/12142458833428315778/js/prettify/prettify.js"></script>
<script type="text/javascript">prettyPrint();</script>


<script src="http://www.gstatic.com/codesite/ph/12142458833428315778/js/source_file_scripts.js"></script>

 <script type="text/javascript" src="https://kibbles.googlecode.com/files/kibbles-1.3.3.comp.js"></script>
 <script type="text/javascript">
 var lastStop = null;
 var initialized = false;
 
 function updateCursor(next, prev) {
 if (prev && prev.element) {
 prev.element.className = 'cursor_stop cursor_hidden';
 }
 if (next && next.element) {
 next.element.className = 'cursor_stop cursor';
 lastStop = next.index;
 }
 }
 
 function pubRevealed(data) {
 updateCursorForCell(data.cellId, 'cursor_stop cursor_hidden');
 if (initialized) {
 reloadCursors();
 }
 }
 
 function draftRevealed(data) {
 updateCursorForCell(data.cellId, 'cursor_stop cursor_hidden');
 if (initialized) {
 reloadCursors();
 }
 }
 
 function draftDestroyed(data) {
 updateCursorForCell(data.cellId, 'nocursor');
 if (initialized) {
 reloadCursors();
 }
 }
 function reloadCursors() {
 kibbles.skipper.reset();
 loadCursors();
 if (lastStop != null) {
 kibbles.skipper.setCurrentStop(lastStop);
 }
 }
 // possibly the simplest way to insert any newly added comments
 // is to update the class of the corresponding cursor row,
 // then refresh the entire list of rows.
 function updateCursorForCell(cellId, className) {
 var cell = document.getElementById(cellId);
 // we have to go two rows back to find the cursor location
 var row = getPreviousElement(cell.parentNode);
 row.className = className;
 }
 // returns the previous element, ignores text nodes.
 function getPreviousElement(e) {
 var element = e.previousSibling;
 if (element.nodeType == 3) {
 element = element.previousSibling;
 }
 if (element && element.tagName) {
 return element;
 }
 }
 function loadCursors() {
 // register our elements with skipper
 var elements = CR_getElements('*', 'cursor_stop');
 var len = elements.length;
 for (var i = 0; i < len; i++) {
 var element = elements[i]; 
 element.className = 'cursor_stop cursor_hidden';
 kibbles.skipper.append(element);
 }
 }
 function toggleComments() {
 CR_toggleCommentDisplay();
 reloadCursors();
 }
 function keysOnLoadHandler() {
 // setup skipper
 kibbles.skipper.addStopListener(
 kibbles.skipper.LISTENER_TYPE.PRE, updateCursor);
 // Set the 'offset' option to return the middle of the client area
 // an option can be a static value, or a callback
 kibbles.skipper.setOption('padding_top', 50);
 // Set the 'offset' option to return the middle of the client area
 // an option can be a static value, or a callback
 kibbles.skipper.setOption('padding_bottom', 100);
 // Register our keys
 kibbles.skipper.addFwdKey("n");
 kibbles.skipper.addRevKey("p");
 kibbles.keys.addKeyPressListener(
 'u', function() { window.location = detail_url; });
 kibbles.keys.addKeyPressListener(
 'r', function() { window.location = detail_url + '#publish'; });
 
 kibbles.keys.addKeyPressListener('j', gotoNextPage);
 kibbles.keys.addKeyPressListener('k', gotoPreviousPage);
 
 
 }
 </script>
<script src="http://www.gstatic.com/codesite/ph/12142458833428315778/js/code_review_scripts.js"></script>
<script type="text/javascript">
 function showPublishInstructions() {
 var element = document.getElementById('review_instr');
 if (element) {
 element.className = 'opened';
 }
 }
 var codereviews;
 function revsOnLoadHandler() {
 // register our source container with the commenting code
 var paths = {'svn55': '/trunk/geochat/json.py'}
 codereviews = CR_controller.setup(
 {"token":"708e9ae8037a1f62ca964109d225650f","assetHostPath":"http://www.gstatic.com/codesite/ph","domainName":null,"assetVersionPath":"http://www.gstatic.com/codesite/ph/12142458833428315778","projectName":"google-app-engine-samples","projectHomeUrl":"/p/google-app-engine-samples","absoluteBaseUrl":"http://code.google.com","relativeBaseUrl":"","urlPrefix":"p","loggedInUserEmail":"mattnashbrowns@gmail.com"}, '', 'svn55', paths,
 CR_BrowseIntegrationFactory);
 
 codereviews.registerActivityListener(CR_ActivityType.REVEAL_DRAFT_PLATE, showPublishInstructions);
 
 codereviews.registerActivityListener(CR_ActivityType.REVEAL_PUB_PLATE, pubRevealed);
 codereviews.registerActivityListener(CR_ActivityType.REVEAL_DRAFT_PLATE, draftRevealed);
 codereviews.registerActivityListener(CR_ActivityType.DISCARD_DRAFT_COMMENT, draftDestroyed);
 
 
 
 
 
 
 
 var initialized = true;
 reloadCursors();
 }
 window.onload = function() {keysOnLoadHandler(); revsOnLoadHandler();};

</script>
<script type="text/javascript" src="http://www.gstatic.com/codesite/ph/12142458833428315778/js/dit_scripts.js"></script>

 
 
 <script type="text/javascript" src="http://www.gstatic.com/codesite/ph/12142458833428315778/js/core_scripts.js"></script>
 <script type="text/javascript" src="/js/codesite_product_dictionary_ph.pack.04102009.js"></script>
</div> 
<div id="footer" dir="ltr">
 
 <div class="text">
 
 &copy;2011 Google -
 <a href="/projecthosting/terms.html">Terms</a> -
 <a href="http://www.google.com/privacy.html">Privacy</a> -
 <a href="/p/support/">Project Hosting Help</a>
 
 </div>
</div>
 <div class="hostedBy" style="margin-top: -20px;">
 <span style="vertical-align: top;">Powered by <a href="http://code.google.com/projecthosting/">Google Project Hosting</a></span>
 </div>
 
 


 
 </body>
</html>

