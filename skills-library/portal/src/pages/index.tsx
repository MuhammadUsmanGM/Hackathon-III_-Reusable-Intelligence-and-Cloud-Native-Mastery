import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__tagline">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Explore Mastery Catalog - 5min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Documentation for autonomous agentic skills and cloud-native mastery.">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container" style={{padding: '4rem 0', textAlign: 'center'}}>
            <div className="row">
               <div className="col col--4">
                  <div className="text--center">
                    <span style={{fontSize: '4rem'}}>🤖</span>
                  </div>
                  <div className="text--center padding-horiz--md">
                    <Heading as="h3">Agent-Ready</Heading>
                    <p>Built for Claude Code and Goose. Optimized for zero-token logic discovery.</p>
                  </div>
               </div>
               <div className="col col--4">
                  <div className="text--center">
                    <span style={{fontSize: '4rem'}}>☁️</span>
                  </div>
                  <div className="text--center padding-horiz--md">
                    <Heading as="h3">Cloud Native</Heading>
                    <p>Native support for Dapr, Kafka, and Kubernetes orchestration.</p>
                  </div>
               </div>
               <div className="col col--4">
                  <div className="text--center">
                    <span style={{fontSize: '4rem'}}>⚡</span>
                  </div>
                  <div className="text--center padding-horiz--md">
                    <Heading as="h3">MCP Powered</Heading>
                    <p>Utilizes Model Context Protocol for deterministic code execution.</p>
                  </div>
               </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
